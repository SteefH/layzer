"""
LINQ-like goodies for iterables
"""

import itertools


class enumerable(object):


    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)

    def where(self, predicate):
        """
        Filter the contents of the enumerable using a predicate function
        that returns true for the items to keep, and return a new enumerable
        """
        return enumerable(itertools.ifilter(predicate, self))

    def select(self, function):
        """
        Map a function to each item in the enumerable and return a new
        enumerable with the results
        """
        return enumerable(itertools.imap(function, self))

    def _selectmany_generator(self, function):
        for result_list in self.select(function):
            for item in result_list:
                yield item

    def selectmany(self, function):
        """
        Concatenate the iterables in the enumerable and return a new enumerable
        containing the flattened results
        """
        return enumerable(self._selectmany_generator(function))

    def forEach(self, function):
        """
        For each item in the enumerable, call a function which receives the
        item as the first argument, and return the enumerable itself
        """
        return self.select(lambda arg: (function(arg) and False) or arg)

    def execute(self):
        """
        Iterate over all items in the enumerable, triggering all eventual side
        effects that are deferred until evaluation of the enumerable
        """
        for item in self:
            pass

    def sort(self):
        return enumerable(sorted(self))

    def to_list(self):
        return list(self)
