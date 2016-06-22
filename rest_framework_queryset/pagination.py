# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.pagination import BasePagination, PageNumberPagination, LimitOffsetPagination


class HybridPagination(BasePagination):
    proxy = PageNumberPagination()
    limit_offset_pagination = LimitOffsetPagination()

    def paginate_queryset(self, queryset, request, view=None):
        if 'offset' in request.GET:
            self.proxy = self.limit_offset_pagination
        return self.proxy.paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return self.proxy.get_paginated_response(data)

    def to_html(self):
        return self.proxy.to_html()

    def get_results(self, data):
        return self.proxy.get_results(data)
