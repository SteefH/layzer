from django.core.exceptions import MiddlewareNotUsed

class DependencyInjectionMiddleware(object):

    def __init__(self):
        import layzer.startup
        # to stop further calls to this middleware
        raise MiddlewareNotUsed
