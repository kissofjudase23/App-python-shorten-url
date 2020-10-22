class EntitryMixin(object):
    def to_dict(self):
        return dict(
            (key, getattr(self, key)) for key in dir(self) if key not in dir(self.__class__)
        )
