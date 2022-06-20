from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.core import serializers
from django.core.serializers.python import Serializer


class JsonSerializer(Serializer):
    # pass

    def get_dump_object(self, obj):
        return {}

    # def end_object( self, obj ):
    #     self._current['id'] = obj._get_pk_val()
    #     self._current.update(self.get_dump_object(obj) or {})
    #     self.objects.append( self._current )


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(context,)

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        return context


class JsonListView(JSONResponseMixin, DetailView):
    fields = None
    model = None
    prop = 'object_list'

    def get_dump_object(self, obj):
        keys = self.fields or '__all__'

        if keys == '__all__':
            r = ()
            for field in self.model._meta.fields:
                r += (field.attname, )
            keys = r
        return { x: getattr(obj, x) for x in keys}

    def get_results(self):
        return self.model.objects.all()

    def get_serialiser(self):
        serial_data = JsonSerializer()
        serial_data.get_dump_object = self.get_dump_object
        return serial_data

    def get(self, request, *args, **kwargs):
        serial = self.get_serialiser()
        result = self.get_results()
        r = serial.serialize(result)
        data = {
            self.prop:r
        }
        return self.render_to_json_response(data, **kwargs)


class JsonDetailView(JsonListView):
    prop = 'object'

    def get_results(self):
        return self.model.objects.get(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        serial = self.get_serialiser()
        result = self.get_results()
        r = serial.serialize([result])
        data = {
            self.prop:r[0]
        }
        return self.render_to_json_response(data, **kwargs)
