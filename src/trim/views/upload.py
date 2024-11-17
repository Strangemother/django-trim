from pathlib import Path
import uuid

from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from ..forms.upload import FileChunkForm, FilesForm, FileForm, MergeConfirmForm
from .base import FormView, TemplateView

import os
import json
from django.urls import reverse
from ..merge import recombine, FileExists

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent
UPLOADS = ROOT / "uploads"

# fs = FileSystemStorage(location=UPLOADS)

cache = {}


def get_cache():
    return cache


def unlink_dir_files(dir_path):
    res = ()
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            os.unlink(os.path.join(root, f))
            # res += (Path(f).relative_to(dir_path),)
            res += (f,)
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
            # res += (Path(d).relative_to(dir_path),)
            res += (d,)

    c = 0
    for root, dirs, files in os.walk(dir_path):
        c += len(files)
        c += len(dirs)

    return {
        'files': res,
        'old_count': len(res),
        'new_count': c,
    }


def verify_file(asset):
    res = {
        'size': asset['output']['size'] == asset['bytesize']
    }

    return res


class AssetMixin(object):

    upload_dir_settings_key = 'CHUNK_UPLOAD_DIR'

    def get_uuid(self):
        return self.kwargs['uuid']

    def get_asset(self):
        return cache[self.get_uuid()]

    def ensure_dir(self, location):
        fullpath = location
        print('Destination', fullpath)

        if fullpath.exists() is False:
            fullpath.mkdir(parents=True)
            print(fullpath)
        return fullpath

    def get_upload_dir(self):
        # HERE = Path(__file__).parent
        # ROOT = HERE.parent.parent.parent
        # UPLOADS = ROOT / "uploads"
        return getattr(settings, self.upload_dir_settings_key)

    def get_fs(self):
        uploads = self.get_upload_dir()
        return FileSystemStorage(location=uploads)

    def get_current_username(self):
        username = self.request.user.username
        if len(username) == 0 and self.request.user.is_anonymous:
            username = 'anonymous'
        return username

    def get_parts_dir(self):
        file_uuid = self.get_uuid()
        info = cache[file_uuid]
        name = info['internal_name']
        suffix = info['suffix']
        username = self.get_current_username()
        make_name = Path(username) / file_uuid
        return make_name


class UploadAssetView(FormView, AssetMixin):
    """An upload file form view, with two forms.
    """
    form_class = FileForm
    template_name = "trim/upload/upload_view.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['file_chunk_form'] = FileChunkForm
        return kwargs

    def save_asset(self, data):
        file_uuid = str(uuid.uuid4())
        filename = data['filename']
        if len(filename) == 0:
            filename = "foo.unknown"

        suffix = Path(data['filepath']).suffix
        name = Path(data['filename']).stem
        cache = get_cache()
        cache[file_uuid] = {
            'filetype': data['filetype'],
            'bytesize': data['byte_size'],
            'filepath': data['filepath'],
            'suffix': suffix,
            'internal_name': name,
            'done': False,
        }

        cache[file_uuid]['filename'] = filename
        return file_uuid

    def form_valid(self, form):
        """Return an ajax response of content
        for the incoming chunks
        """
        data = form.cleaned_data
        file_uuid = self.save_asset(data)

        return JsonResponse({
                'ok': True,
                'file_uuid': file_uuid,
        })


class UploadAssetSuccessView(TemplateView, AssetMixin):
    template_name = 'trim/file/upload_success.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['asset'] = self.get_asset()
        return kwargs


@method_decorator(csrf_exempt, name="dispatch")
class UploadChunkView(FormView, AssetMixin):
    form_class = FileChunkForm
    template_name = "trim/upload/upload_chunk_view.html"

    def ensure_fullpath(self, filename):
        fs = self.get_fs()
        location = Path(fs.location)
        fullpath = location / filename

        print('Location', location)
        print('Destination', fullpath)

        if fullpath.parent.exists() is False:
            if location.exists():
                # ensure the parent is set correctly.
                v = fullpath.relative_to(location)
                fullpath.parent.mkdir(parents=True)
                print(v)
        return fullpath

    def save_file_part(self, data):
        store_path = self.generate_store_path(data)
        # The stream chunk of file
        filepart = data['filepart']
        ok = self.write_file(filepart, store_path)
        return ok

    def generate_store_path(self, data):
        username = self.get_current_username()

        info = cache.get(file_uuid)
        # The mapped name given to the form before the main upload
        name = info['internal_name']
        suffix = info['suffix']


        # returned from the upload asset initial view.
        file_uuid = data['file_uuid']
        # The int chunk index
        index = data['chunk_index']
        # The 'part' defines an extended suffix,
        # to flag this is a partial file.
        part = f".part_{index}"
        filename = f"{name}{suffix}{part}" # received file name
        make_name = Path(username) / file_uuid / filename
        # fs.location is enforced.
        store_path = self.ensure_fullpath(make_name)
        return store_path

    def form_valid(self, form):
        data = form.cleaned_data
        ok = self.save_file_part(data)

        return JsonResponse({
                'ok': True
            })

    def write_file(self, file, store_path, storage=None):
        print('Writing', store_path)
        storage = storage or self.get_fs()
        # with fs.open(store_path, 'wb+') as stream:
        with storage.open(store_path, 'wb+') as stream:
            for chunk in file.chunks():
                stream.write(chunk)
        return store_path.exists()


class MergeAssetView(FormView, AssetMixin):

    form_class = MergeConfirmForm
    # template_name = "corsa/form.html"
    template_name = "trim/file/merge_view.html"
    skip_step = False

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        ctx = self.get_context_data()
        if self.skip_step:
            # Perform auto valid form
            # form = ctx['form']
            form_class = self.get_form_class()
            form = form_class({"delete_cache": True, 'confirm_merge': True})
            assert form.is_valid()
            return self.form_valid(form)
        return self.render_to_response(ctx)

    def get_success_url(self):
        args = (self.get_uuid(),)
        return reverse('file:upload_success', args=args)

    def get_out_dir(self):
        fs = self.get_fs()
        out_path = Path(fs.location) / 'finished' / self.get_current_username()
        return out_path

    def form_valid(self, form):
        # Confirm post to merge the attached asset
        data = form.cleaned_data
        accept = data['confirm_merge']
        delete_cache = data['delete_cache']

        if not accept:
            return super().form_valid(form)

        ok = self.perform_all(delete_cache)

        if ok:
            return super().form_valid(form)

        print('Bad Path.')
        return super().form_valid(form)

    def perform_all(self, delete_cache=False):
        asset = self.get_asset()
        perform_asset = self.resolve_paths()
        asset['input'] = perform_asset

        dir_path = perform_asset['path']

        if dir_path.exists():
            output = self.perform(asset, dir_path, out_path)
            asset['output'] = output
            if delete_cache:
                self.delete_cache(asset)
            return True
            # return super().form_valid(form)
        return False

    def resolve_paths(self):

        out_path = self.get_out_dir()
        self.ensure_dir(out_path)
        fs = self.get_fs()

        return {
            "path": Path(fs.location) / self.get_parts_dir(),
            "output_path": out_path,
        }

    def delete_cache(self, asset):
        # delete the merge parts.
        print('Delete')
        p = Path(asset['input']['path'])
        if p.exists() and p.is_dir():
            # scrub it
            print('Delete', p)
            deleted = unlink_dir_files(p)
            asset['deletion'] = deleted
            receipt = p / 'delete-receipt.json'
            receipt.write_text(json.dumps(deleted, indent=4))
        return p.exists() is False

    def perform(self, asset, dir_path, out_path):
        try:
            output_path = recombine(dir_path, out_path)
        except FileExists as err:
            output_path = err.args[0]

        output_path = Path(output_path)
        fs = self.get_fs()

        result = {
            "path": output_path.relative_to(fs.location).as_posix(),
            "exists": output_path.exists(),
            "size": os.path.getsize(output_path),
            'sub_path': output_path.relative_to(out_path).as_posix(),
            'uuid': self.get_uuid(),
        }

        result['output_path'] = Path(result['output']['path']).as_posix()
        result['done'] = True
        result['verification'] = verify_file(result)

        return result

