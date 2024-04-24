from django import forms
from trim.forms import fields


def file_upload_loc(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format('uploads/', filename)
    # return "user_{0}/{1}".format(instance.user.id, filename)


"""
1. serve a form with all the fields.
2. on post, edit the form in js
2. Post js file reader responses to the chunk form
    Each chunk response returns an update result
"""

class FilesForm(forms.Form):
    """A Meta form is served in parallel to the file upload
    The meta should receive an upload ID, stored with the
    asset to the temp location until required.
    """
    filename = fields.chars(max_length=255, required=False)
    file = fields.file(required=False)

    byte_size = fields.hidden(fields.int(required=False))
    filepath = fields.hidden(fields.chars(max_length=255, required=False))
    filetype = fields.hidden(fields.chars(max_length=255, required=False))

    # class Meta:
    #     fields = ('query',)


class FileChunkForm(forms.Form):
    """The JS chunking serves the FilesForm to receive additional
    parameters for this form.

    The JS slices the file into chunks, posting many chunks to this endpoint.
    """
    # chunk_id = forms.CharField()

    # The file_uuid is populated by the response from the FilesForm
    # Used to track a single upload
    file_uuid = forms.CharField()
    # The numerical index of the chunk - managed by the JS
    chunk_index = fields.integer()
    # The 'file' expecting bytes for a partial file
    filepart = fields.file()

    # class Meta:
    #     fields = ('query',)


class MergeConfirmForm(forms.Form):
    confirm_merge = fields.bool_true()
    delete_cache = fields.bool_true()