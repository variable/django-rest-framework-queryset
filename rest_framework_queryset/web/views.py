from django.shortcuts import render
from django.views.generic import ListView
from queryset import APIQuerySet


class ListDataView(ListView):
    paginate_by = 10
    template_name = 'list.html'

    def get_queryset(self, *args, **kwargs):
        return APIQuerySet('http://localhost:8082/api/')
