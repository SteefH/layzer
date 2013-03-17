import inspect

class Singleton(object):

    def __init__(self, item):
        self.item = item

    def instantiate(self):
        return self.item()

class Registry(object):
    _mapping = {}
    _registry = []

    def _rebuildmapping(self):
        result = {}
        for r in self._registry:
            result.update(r)
        self._mapping = result

    def register(self, mapping):
        self._registry.append(mapping)
        self._rebuildmapping()

    def unregister(self, mapping):

        self._mapping = [m for m in self._mapping if m is not mapping]
        self._rebuildmapping()

    def inject(self, fn):
        argspec = inspect.getargspec(fn)
        def decorator(*args, **kwds):
            arg_counter = 0
            newargs = []
            for a in argspec.args:
                if a in self._mapping:
                    newargs.append(self.get(a))
                else:
                    try:
                        arg = args[arg_counter]
                    except IndexError:
                        raise TypeError('No value given for ' + a)
                    newargs.append(arg)
                    arg_counter += 1
            return fn(*newargs, **kwds)
        decorator.__name__ = fn.__name__
        decorator.__doc__ = fn.__doc__
        return decorator

    def get(self, item):
        value = self._mapping[item]
        if isinstance(value, Singleton):
            value = value.instantiate()
            self._mapping[item] = value
        return value

_registry = Registry()

register = _registry.register
unregister = _registry.unregister
inject = _registry.inject
get = _registry.get
