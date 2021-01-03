from django.views.generic import TemplateView

from .models import TestModel


class TestModelListView(TemplateView):

    template_name = 'testapp/list.html'

    def get_context_data(self, **kwargs):
        data = super(TestModelListView, self).get_context_data(**kwargs)
        data.update({'object_list': TestModel.objects.all()})
        return data
