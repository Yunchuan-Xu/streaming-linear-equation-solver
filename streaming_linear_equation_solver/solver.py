from collections import defaultdict
from typing import Dict, Union

from .const import Const
from .linear_sum import LinearSum


class Unit:
    def __repr__(self):
        return '1'

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return True


class Solver:
    def __init__(self, constants: Dict[str, Union[int, float, Const]]=None, verbose: int=0):
        """

        :param constants: pre-defined variables with known value
                          keys are variable names, values are known values
        :param verbose: 0 or 1
        """
        self.verbose = verbose
        self.unit = Unit()
        self.constants = {} if constants is None else constants
        self.references = defaultdict(set)
        self.substitutions = {}

    def print(self, level: int, msg: str):
        if self.verbose >= level:
            print(msg)

    def eval(self, expression: LinearSum):
        if len(expression) == 0:
            return 0
        elif len(expression) == 1 and self.unit in expression:
            return expression[self.unit]

    def input(self, lhs: Dict[str, Union[int, float, Const]], rhs: Union[int, float, Const]):
        """
        input an equation where left hand side is linear sum of variable terms and right hand side is a constant term
        
        :param lhs: variable terms
                    keys are variable names, values are multiplication factors
        :param rhs: constant term
        """
        # prepare expression
        lhs[self.unit] = -rhs
        expr = LinearSum(lhs)
        self.print(1, 'raw expr: {}'.format(expr))

        # substitute variables in the expression
        for variable in list(expr.terms):
            if variable in self.substitutions:
                expr.substitute(variable, self.substitutions[variable])
            elif variable in self.constants:
                expr.substitute(variable, LinearSum({self.unit: self.constants[variable]}))
        self.print(1, 'sub expr: {}'.format(expr))

        # choose target variable
        var = None
        for variable in expr.terms:
            if variable != self.unit:
                var = variable
                if variable not in self.references:
                    break
        if var is None:
            self.print(1, 'redundant equation\n')
            return

        # solve target expression
        expr.solve(var)
        val = self.eval(expr)
        self.print(1, 'var equation: {} = {}'.format(var, expr))

        # update target variable
        if val is None:
            self.substitutions[var] = expr
            for gval in expr.terms:
                if gval != self.unit:
                    self.references[gval].add(var)
        else:
            self.constants[var] = val

        # update referenced variables
        if var in self.references:
            for svar in self.references.pop(var):
                self.substitutions[svar].substitute(var, expr)
                val = self.eval(self.substitutions[svar])
                if val is not None:
                    self.constants[svar] = self.substitutions.pop(svar)[self.unit]

        self.print(1, 'constants: {}'.format(self.constants))
        self.print(1, 'references: {}'.format(repr(self.references)[27: -1]))
        self.print(1, 'substitutions: {}\n'.format(self.substitutions))
