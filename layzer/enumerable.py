import itertools


class enumerable(object):

    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)

    def where(self, predicate):
        return enumerable(itertools.ifilter(predicate, self))

    def select(self, function):
        return enumerable(itertools.imap(function, self))

    def _selectmany_generator(self, function):
        for result_list in self.select(function):
            for item in result_list:
                yield item

    def selectmany(self, function):
        return enumerable(self._selectmany_generator(function))

    def forEach(self, function):
        return self.select(lambda arg: (function(arg) and False) or arg)

    def execute(self):
        for item in self:
            pass

    def sort(self):
        return enumerable(sorted(self))

    def to_list(self):
        return list(self)
