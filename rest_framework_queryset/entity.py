import requests


class EntityMixin(object):

    def save(self):
        requests.put(self.url, data=self)


def get_entity(obj):
    class Entity(obj.__class__, EntityMixin):
        pass

        def save(self):
            requests.put(self.url, data=self)

    return Entity(obj)
