# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import


class APISearchableMixin(object):
    # request fields that we are interested in
    search_fields = []

    def __init__(self, *args, **kwargs):
        super(APISearchableMixin, self).__init__(*args, **kwargs)
        self._search_params = {}

    def get_context_data(self, *args, **kwargs):
        """
        put search_fields into ctx
        """
        ctx = super(APISearchableMixin, self).get_context_data(*args, **kwargs)
        ctx['search_fields'] = self.get_search_params()
        return ctx

    def get_search_params(self):
        for field in self.search_fields:
            if self.request.method == 'POST':
                self._search_params[field] = self.request.POST.get('__search_{}'.format(field), '')
            if self.request.method == 'GET':
                self._search_params[field] = self.request.GET.get(field, '')
        return self._search_params

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
