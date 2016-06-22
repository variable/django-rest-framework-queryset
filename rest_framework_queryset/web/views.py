from django.shortcuts import render
from django.views.generic import ListView
from queryset import RestFrameworkQuerySet


class ListDataView(ListView):
    paginate_by = 10
    template_name = 'list.html'

    def get_queryset(self, *args, **kwargs):
        return RestFrameworkQuerySet('http://localhost:8082/api/').filter(**self.request.GET.dict())
