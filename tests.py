# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.test import TestCase, LiveServerTestCase
from django.core.paginator import Paginator
from django.core.exceptions import MultipleObjectsReturned
from api.models import DataModel
from rest_framework_queryset import RestFrameworkQuerySet
from mock import patch, MagicMock


class RestFrameworkQuerySetTestCase(TestCase):

    def test_filter(self):
        qs = RestFrameworkQuerySet('/api/')
        qs1 = qs.filter(a=123)
        self.assertTrue('params' not in qs.kwargs, "qs should not have params set as it's cloned in filter()")
        self.assertEqual(qs1.kwargs['params']['a'], 123)

    def test_filter_chain(self):
        qs = RestFrameworkQuerySet('/api/')
        qs1 = qs.filter(a=123)
        self.assertEqual(qs1.kwargs['params']['a'], 123)
        qs2 = qs1.filter(b=234)
        self.assertEqual(qs2.kwargs['params']['b'], 234)

        qs = RestFrameworkQuerySet('/api/')
        qs1 = qs.filter(a=123).filter(b=234)
        self.assertEqual(qs1.kwargs['params']['a'], 123)
        self.assertEqual(qs1.kwargs['params']['b'], 234)

    def test_filter_call(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': range(10)})
        with patch('rest_framework_queryset.queryset.requests.Session.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/')
            qs1 = qs.filter(a=123)
            self.assertEqual(list(qs1), list(range(10)))
            mock_get.assert_any_call('/api/', params={'a': 123, 'offset': 0, 'limit': 10})
            qs2 = qs1.filter(b=234)
            list(qs2)  # execute
            mock_get.assert_any_call('/api/', params={'a': 123, 'b': 234, 'offset': 0, 'limit': 10})

    def test_get_call(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': list(range(10))})
        with patch('rest_framework_queryset.queryset.requests.Session.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/')
            with self.assertRaises(MultipleObjectsReturned):
                qs1 = qs.get(a=123)
            self.assertEqual(list(qs), list(range(10)))
            mock_get.assert_any_call('/api/', params={'a': 123})

    def test_get_call_by_id(self):
        fake_response = MagicMock(json=lambda:{'a': 123})
        with patch('rest_framework_queryset.queryset.requests.Session.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/')
            qs1 = qs.get(123)
            self.assertEqual(qs1, {'a': 123})
            mock_get.assert_any_call('/api/123', params={})

    def test_count_call(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': range(10)})
        with patch('rest_framework_queryset.queryset.requests.Session.get', return_value=fake_response) as mock_get:
            count = RestFrameworkQuerySet('/api/').count()
            self.assertEqual(count, 10)

    def test_all(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': range(10)})
        with patch('rest_framework_queryset.queryset.requests.Session.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/').all()
            self.assertEqual(list(qs), list(range(10)))


class APILiveServerTestCase(LiveServerTestCase):
    def test_pagination(self):
        for i in range(100):
            DataModel.objects.create(value=i)
        qs = RestFrameworkQuerySet('{}/api/'.format(self.live_server_url))
        p = Paginator(qs, 10)
        self.assertEqual(p.count, 100)
        self.assertEqual(p.num_pages, 10)
        page2 = p.page(2)
        item_list = [item['value'] for item in page2.object_list]
        self.assertEqual(item_list, list(range(10, 20)))

    def test_list_all(self):
        DataModel.objects.bulk_create([DataModel(value=i) for i in range(1000)])
        qs = RestFrameworkQuerySet('{}/api/'.format(self.live_server_url))
        item_list = [item['value'] for item in list(qs)]
        self.assertEqual(item_list, list(range(1000)))

    def test_list_filter(self):
        DataModel.objects.bulk_create([DataModel(value=i) for i in range(1000)])
        qs = RestFrameworkQuerySet('{}/api/'.format(self.live_server_url))
        qs = qs.filter(value__gt=300)
        item_list = [item['value'] for item in list(qs)]
        self.assertEqual(item_list, list(range(301, 1000)))

    def test_slice(self):
        DataModel.objects.bulk_create([DataModel(value=i) for i in range(1000)])
        qs = RestFrameworkQuerySet('{}/api/'.format(self.live_server_url))
        item_list = [item['value'] for item in qs[200:1000]]
        self.assertEqual(item_list, list(range(200, 1000)))
