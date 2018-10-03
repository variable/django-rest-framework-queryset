# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator
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
        return iter(self.get_result())

    def __len__(self):
        return self.count()

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get_result()[index]
        elif isinstance(index, slice):
            return self.page_result(index)

    def _clone(self):
        kwargs = copy.deepcopy(self.kwargs)
        args = copy.deepcopy(self.args)
        url = copy.copy(self.url)
        cloned = self.__class__(url, *args, **kwargs)
        cloned.request_method = self.request_method
        return cloned

    def count(self):
        raise NotImplementedError()

    def filter(self, **kargs):
        raise NotImplementedError()

    def all(self, **kargs):
        raise NotImplementedError()

    def get_result(self):
        raise NotImplementedError()

    def page_result(self):
        raise NotImplementedError()


class RestFrameworkQuerySet(BaseAPIQuerySet):
    def __iter__(self):
        paginator = Paginator(self, 100)
        for page in paginator.page_range:
            for item in paginator.page(page).object_list:
                yield item

    def count(self):
        cloned = self._clone()
        params = cloned.kwargs.get('params', {})
        params['offset'] = 0
        params['limit'] = 0
        resp = cloned.call_api()
        result = resp.json()
        return result['count']

    def get_result(self):
        response = self.call_api()
        result = response.json()
        return result['results']

    def page_result(self, slicer):
        cloned = self._clone()
        params = cloned.kwargs.setdefault('params', {})
        params['offset'] = slicer.start
        params['limit'] = slicer.stop - slicer.start
        return cloned.get_result()

    def filter(self, **kwargs):
        cloned = self._clone()
        params = cloned.kwargs.setdefault('params', {})
        params.update(kwargs)
        return cloned

    def get(self, **kwargs):
        cloned = self.filter(**kwargs)
        result = cloned.get_result()
        if len(result) > 1:
            raise MultipleObjectsReturned('get() returned more than one result, it returned {}'.format(cloned.count()))
        return result[0]

    def all(self):
        return self._clone()
