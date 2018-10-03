from django.shortcuts import render
from django.views.generic import ListView
from rest_framework_queryset import RestFrameworkQuerySet


class ListDataView(ListView):
    paginate_by = 10
    template_name = 'list.html'

    def get_queryset(self, *args, **kwargs):
        return RestFrameworkQuerySet('{}/api/'.format(self.request.META['SERVER_URL'])).filter(**self.request.GET.dict())
