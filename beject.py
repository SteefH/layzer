import inspect
import functools

class Singleton(object):

    def __init__(self, item):
        self.item = item

    def instantiate(self):
        return self.item()

def compose(*args):
    fns = list(args)
    f1 = fns.pop()
    fns.reverse()
    def call(*args, **kwds):
        return functools.reduce(
            (lambda result, fn: fn(result)), fns, f1(*args, **kwds)
        )
    return call

def compose_with(*superargs):
    def call(*args):
        return compose(*(superargs + args))
    return call

@compose_with(property)
class _lazyprop(object):

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwds):
        try:
            return self.value
        except AttributeError:
            pass
        self.value = self.fn(*args, **kwds)
        return self.value

def ignore_args(fn):
    def call(*_, **__):
        return fn()
    return call

class Registry(object):
    _mapping = {}
    _registry = []
    _defined = {}

    def _rebuildmapping(self):
        result = {}
        result.update(self._defined)
        for r in self._registry:
            result.update(r)
        self._mapping = result

    def register(self, mapping):
        self._registry.append(mapping)
        self._rebuildmapping()

    def unregister(self, mapping):

        self._mapping = [m for m in self._mapping if m is not mapping]
        self._rebuildmapping()

    def _attr_inject(self, *args, **kwds):
        def decorator(fn):
            def createprop(f):
                return _lazyprop(ignore_args(lambda: self.get(f)))
            for field in args:
                setattr(fn, field, createprop(field))
            for name, value in kwds.items():
                setattr(fn, name, createprop(value))
            return fn
        return decorator


    def _args_inject(self, fn):
        argspec = inspect.getargspec(fn)
        @functools.wraps(fn)
        def decorator(*args, **kwds):
            if not kwds:
                kwds = {}
            else:
                kwds = kwds.copy()
            for a in argspec.args:
                if a in self._mapping:
                    kwds[a] = self.get(a)
            return fn(*args, **kwds)
        return decorator

    def inject(self, *args, **kwds):
        if len(args) == 1 and inspect.isroutine(args[0]):
            return self._args_inject(args[0])
        return self._attr_inject(*args, **kwds)

    def get(self, item):
        value = self._mapping[item]
        if isinstance(value, Singleton):
            value = value.instantiate()
            self._mapping[item] = value
        return value

    def define(self, name, modifier=None):
        def decorator(fn):
            val = fn
            if modifier:
                val = modifier(val)
            self._defined[name] = val
            return fn
        return decorator

_registry = Registry()

register = _registry.register
unregister = _registry.unregister
inject = _registry.inject
get = _registry.get
define = _registry.define

