import json
from abc import abstractmethod
from shorten_url.pattern import SingletonABCMeta


class CacheABC(metaclass=SingletonABCMeta):

    @abstractmethod
    def set(self, key, val, *, ex=None):
        raise NotImplementedError()

    @abstractmethod
    def get(self, key):
        raise NotImplementedError()

    def set_json(self, key, val, *, ex=None):
        self.set(key, json.dumps(val), ex=ex)

    def get_json(self, key):
        val = self.get(key)

        if not val:
            return None

        return json.loads(val)
