# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class HybridPagination(PageNumberPagination):
    """
    Basically allows both pagination method to work within a single pagination class.
    By default it uses the PageNumberPagination
    When 'offset' is used in request.GET, it will switch to use LimitOffsetPagination
    """
    page_size = 10
    default_limit = 1

    def __init__(self, *args, **kwargs):
        self.proxy = None
        return super(HybridPagination, self).__init__(*args, **kwargs)

    def paginate_queryset(self, queryset, request, view=None):
        if 'offset' in request.GET or 'limit' in request.GET:
            self.proxy = LimitOffsetPagination()
            return self.proxy.paginate_queryset(queryset, request, view)
        return super(HybridPagination, self).paginate_queryset(queryset, request, view)

    def __getattribute__(self, item):
        if item in ['paginate_queryset']:
            return object.__getattribute__(self, item)
        try:
            proxy = object.__getattribute__(self, "proxy")
            return object.__getattribute__(proxy, item)
        except AttributeError:
            return object.__getattribute__(self, item)

