# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class HybridPagination(PageNumberPagination, LimitOffsetPagination):
    """
    Basically allows both pagination method to work within a single pagination class.
    By default it uses the PageNumberPagination
    When 'offset' is used in request.GET, it will switch to use LimitOffsetPagination
    """
    proxy = PageNumberPagination

    def paginate_queryset(self, queryset, request, view=None):
        if 'offset' in request.GET or 'limit' in request.GET:
            self.proxy = LimitOffsetPagination
        return self.proxy.paginate_queryset(self, queryset, request, view)

    def get_paginated_response(self, *args, **kwargs):
        return self.proxy.get_paginated_response(self, *args, **kwargs)

    def to_html(self):
        return self.proxy.to_html(self)

    def get_results(self, *args, **kwargs):
        return self.proxy.get_results(self, *args, **kwargs)

    def get_next_link(self, *args, **kwargs):
        return self.proxy.get_next_link(self, *args, **kwargs)

    def get_previous_link(self, *args, **kwargs):
        return self.proxy.get_previous_link(self, *args, **kwargs)

    def get_html_context(self, *args, **kwargs):
        return self.proxy.get_html_context(self, *args, **kwargs)

