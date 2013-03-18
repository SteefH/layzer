class _lazyproperty(object):
    isset = False
    value = None

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwds):
        if self.isset:
            return self.value
        self.value = self.fn(*args, **kwds)
        self.isset = True
        return self.value

def lazyproperty(fn):
    return property(_lazyproperty(fn))
