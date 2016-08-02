# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.test import TestCase, LiveServerTestCase
from django.core.paginator import Paginator
from django.core.exceptions import MultipleObjectsReturned
from api.models import DataModel
from queryset import RestFrameworkQuerySet
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
        with patch('queryset.requests.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/')
            qs1 = qs.filter(a=123)
            self.assertEqual(list(qs1), range(10))
            mock_get.assert_any_call('/api/', params={'a': 123})
            qs2 = qs1.filter(b=234)
            list(qs2)  # execute
            mock_get.assert_any_call('/api/', params={'a': 123, 'b':234})

    def test_get_call(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': range(10)})
        with patch('queryset.requests.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/')
            with self.assertRaises(MultipleObjectsReturned):
                qs1 = qs.get(a=123)
            self.assertEqual(list(qs), range(10))
            mock_get.assert_any_call('/api/', params={'a': 123})

    def test_count_call(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': range(10)})
        with patch('queryset.requests.get', return_value=fake_response) as mock_get:
            count = RestFrameworkQuerySet('/api/').count()
            self.assertEqual(count, 10)

    def test_all(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': range(10)})
        with patch('queryset.requests.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/').all()
            self.assertEqual(list(qs), range(10))


class PaginationTestCase(LiveServerTestCase):
    def test_pagination(self):
        for i in range(100):
            DataModel.objects.create(value=i)
        qs = RestFrameworkQuerySet('http://localhost:8082/api/')
        p = Paginator(qs, 10)
        self.assertEqual(p.count, 100)
        self.assertEqual(p.num_pages, 10)
        page2 = p.page(2)
        item_list = [item['value'] for item in page2.object_list]
        self.assertEqual(item_list, range(10, 20))
