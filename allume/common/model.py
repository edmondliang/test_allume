import collections


class Model(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = self.__class__(**value)
            elif isinstance(value, list):
                self.__dict__[key] = []
                for item in value:
                    if isinstance(item, dict):
                        self.__dict__[key].append(self.__class__(**item))
                    else:
                        self.__dict__[key].append(item)

    def __setitem__(self, key, value):
        raise Exception('Not allow')

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        raise Exception('Not allow')

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % repr(self.__dict__)
