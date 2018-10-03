from django.test import LiveServerTestCase
from api.models import DataModel


class ListTestCase(LiveServerTestCase):
    def setUp(self):
        # create data
        for i in range(100):
            DataModel.objects.create(value=i)

    def test_list(self):
        resp = self.client.get('/list/', SERVER_URL=self.live_server_url)
        self.assertEqual([v['value'] for v in resp.context['object_list']], [i for i in range(10)])
        resp = self.client.get('/list/page/2/', SERVER_URL=self.live_server_url)
        self.assertEqual([v['value'] for v in resp.context['object_list']], [i for i in range(10, 20)])

    def test_filter(self):
        resp = self.client.get('/list/?value=10', SERVER_URL=self.live_server_url)
        self.assertEqual(len(resp.context['object_list']), 1)
        self.assertEqual(resp.context['object_list'][0]['value'], 10)

    def test_get(self):
        dm = DataModel.objects.first()
        resp = self.client.get('/list/?id={}'.format(dm.id), SERVER_URL=self.live_server_url)
        self.assertEqual(len(resp.context['object_list']), 1)
        self.assertEqual(resp.context['object_list'][0]['value'], dm.value)
