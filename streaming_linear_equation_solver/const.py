import math
from typing import Union


class Const:
    def __init__(self, n: Union[int, float]=0, d: Union[int, float]=1):
        """

        :param n: numerator
        :param d: denominator
        """
        if d == 0:
            raise ValueError('Const can not be initialized with d equals to 0')
        if isinstance(n, int) and isinstance(d, int):
            if d < 0:
                n, d = -n, -d
            gcd = math.gcd(n, d)
            self.n = n // gcd
            self.d = d // gcd
        else:
            self.n = n / d
            self.d = 1

    def __repr__(self):
        return str(self.n) if self.d == 1 else '{}/{}'.format(self.n, self.d)

    def __eq__(self, other):
        if not isinstance(other, Const):
            other = Const(other)
        return self.n == other.n and self.d == other.d

    def __neg__(self):
        return Const(-self.n, self.d)

    def __add__(self, other):
        n1, d1 = self.n, self.d
        n2, d2 = Const._get_n_and_d(other)
        return Const(n1 * d2 + n2 * d1, d1 * d2)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        n1, d1 = self.n, self.d
        n2, d2 = Const._get_n_and_d(other)
        return Const(n1 * d2 - n2 * d1, d1 * d2)

    def __rsub__(self, other):
        n1, d1 = Const._get_n_and_d(other)
        n2, d2 = self.n, self.d
        return Const(n1 * d2 - n2 * d1, d1 * d2)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        n1, d1 = self.n, self.d
        n2, d2 = Const._get_n_and_d(other)
        return Const(n1 * n2, d1 * d2)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        n1, d1 = self.n, self.d
        n2, d2 = Const._get_n_and_d(other)
        return Const(n1 * d2, d1 * n2)

    def __rtruediv__(self, other):
        n1, d1 = self.n, self.d
        n2, d2 = Const._get_n_and_d(other)
        return Const(n2 * d1, d2 * n1)

    def __idiv__(self, other):
        return self.__truediv__(other)

    @property
    def value(self):
        return self.n / self.d

    @staticmethod
    def _get_n_and_d(value):
        if isinstance(value, Const):
            return value.n, value.d
        else:
            return value, 1
