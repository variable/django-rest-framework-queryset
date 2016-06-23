# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import copy


class BaseAPIQuerySet(object):
    def __init__(self, url, *args, **kwargs):
        self.request_method = requests.get
        self.url = url
        self.args = args
        self.kwargs = kwargs

    def call_api(self):
        """
        perform api call
        """
        return self.request_method(self.url, *self.args, **self.kwargs)

    def __iter__(self):
        return iter(self.__call__())

    def __call__(self):
        resp = self.call_api()
        return self.get_result(resp)

    def __len__(self):
        return self.get_count()

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.__call__()[index]
        elif isinstance(index, slice):
            return self.page_result(index)

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

    def filter(self, **kargs):
        raise NotImplementedError()

    def get_count(self):
        raise NotImplementedError()

    def get_result(self):
        raise NotImplementedError()

    def page_result(self):
        raise NotImplementedError()


class RestFrameworkQuerySet(BaseAPIQuerySet):
    def get_count(self):
        with self:
            params = self.kwargs.get('params', {})
            params['offset'] = 0
            params['limit'] = 0
            self.kwargs['params'] = params
            resp = self.call_api()
            result = resp.json()
            return result['count']

    def get_result(self, response):
        result = response.json()
        return result['results']

    def page_result(self, slicer):
        params = self.kwargs.setdefault('params', {})
        params['offset'] = slicer.start
        params['limit'] = slicer.stop - slicer.start
        return self

    def filter(self, **kwargs):
        params = self.kwargs.setdefault('params', {})
        params.update(kwargs)
        return self
