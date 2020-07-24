from collections import defaultdict

from .const import Const


class LinearSum:
    def __init__(self, terms: dict):
        """

        :param terms: key as variable name, value as multiplication factor
        """
        self.terms = defaultdict(Const)
        for (variable, factor) in terms.items():
            if factor != 0:
                self.terms[variable] += factor

    def __repr__(self):
        return ' + '.join('({} * {})'.format(factor, variable) for (variable, factor) in sorted(self.terms.items()))

    def __len__(self):
        return len(self.terms)

    def __getitem__(self, item):
        return self.terms.get(item, 0)

    def __contains__(self, item):
        return item in self.terms

    def __neg__(self):
        return self.__mul__(-1)

    def __add__(self, other):  # other: LinearSum or dict
        new_terms = self.terms.copy()
        if isinstance(other, LinearSum):
            other = other.terms
        elif other == 0:  # be compatible with sum()
            return self
        for (variable, factor) in other.items():
            new_terms[variable] += factor
        return LinearSum(new_terms)

    def __radd__(self, other):  # other: LinearSum or dict
        return self.__add__(other)

    def __iadd__(self, other):  # other: LinearSum or dict
        return self.__add__(other)

    def __sub__(self, other):  # other: LinearSum or dict
        new_terms = self.terms.copy()
        if isinstance(other, LinearSum):
            other = other.terms
        for (variable, factor) in other.items():
            new_terms[variable] -= factor
        return LinearSum(new_terms)

    def __rsub__(self, other):  # other: LinearSum or dict
        if isinstance(other, LinearSum):
            other = other.terms
        new_terms = other.copy()
        for (variable, factor) in self.terms.items():
            new_terms[variable] -= factor
        return LinearSum(new_terms)

    def __isub__(self, other):  # other: LinearSum or dict
        return self.__sub__(other)

    def __mul__(self, other):  # other: Const, int or float
        new_terms = self.terms.copy()
        for variable in new_terms:
            new_terms[variable] *= other
        return LinearSum(new_terms)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.__mul__(Const(1, other))

    def __idiv__(self, other):
        return self.__truediv__(other)

    def pop(self, variable):
        return self.terms.pop(variable)

    def substitute(self, variable, other):
        factor = self.terms.pop(variable)
        result = self + other * factor
        self.terms = result.terms

    def solve(self, variable):
        factor = self.terms.pop(variable)
        result = -self / factor
        self.terms = result.terms
