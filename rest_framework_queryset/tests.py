# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.test import TestCase
from queryset import RestFrameworkQuerySet
from mock import patch, MagicMock


class RestFrameworkQuerySetTestCase(TestCase):

    def test_filter(self):
        qs = RestFrameworkQuerySet('/api/')
        qs = qs.filter(a=123)
        self.assertEqual(qs.kwargs['params']['a'], 123)
        qs = qs.filter(b=234)
        self.assertEqual(qs.kwargs['params']['b'], 234)

    def test_filter_chain(self):
        qs = RestFrameworkQuerySet('/api/')
        qs = qs.filter(a=123).filter(b=234)
        self.assertEqual(qs.kwargs['params']['a'], 123)
        self.assertEqual(qs.kwargs['params']['b'], 234)

    def test_filter_call(self):
        fake_response = MagicMock(json=lambda:{'count': 10, 'results': range(10)})
        with patch('queryset.requests.get', return_value=fake_response) as mock_get:
            qs = RestFrameworkQuerySet('/api/')
            qs.filter(a=123)
            self.assertEqual(qs(), range(10))
            mock_get.assert_any_call('/api/', params={'a': 123})
            qs.filter(b=234)
            mock_get.assert_any_call('/api/', params={'a': 123, 'b':234})
