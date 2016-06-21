# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests


class BaseAPIQuerySet(object):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.args = args
        self.kwargs = kwargs

    def __call(self, *args, **kwargs):
        return requests.get(url, *self.args, **kwargs)

    def __call__(self):
        resp = self.__call()
        result = resp.json()
        return result['results']

    def __len__(self):
        with self:
            params = self.kwargs.get('params', {})
            params['page_size'] = 1
            self.kwargs['params'] = params
            resp = self.__call()
            result = resp.json()
            return result['count']

    def __getitem__(self, index):
        if isinstance(index, int):
            return super(BaseAPIQuerySet, self).__getitem__(index)
        elif isinstance(index, slice):
            with self:
                params = self.kwargs.get('params', {})
                params['offset'] = index.start
                params['limit'] = index.stop - index.start
                self.kwargs['params'] = params
                return self.__call__()

    def __enter__(self):
        # temp swap out kwargs, assign by value and keep the original ref
        self._old_kwargs = self.kwargs
        self.kwargs = copy.deepcopy(self.kwargs)
        self._old_args = self.args
        self.args = copy.deepcopy(self.args)

    def __exit__(self, type, value, traceback):
        # put origin kwargs back
        self.kwargs = self._old_kwargs
        self.args = self._old_args
