from django.test import LiveServerTestCase


class ListTestCase(LiveServerTestCase):

    def test_list(self):
        resp = self.client.get('/')
        self.assertEqual(list(resp.context['object_list']), [{'value': i} for i in range(10)])
        resp = self.client.get('/page/2/')
        self.assertEqual(list(resp.context['object_list']), [{'value': i} for i in range(10, 20)])
