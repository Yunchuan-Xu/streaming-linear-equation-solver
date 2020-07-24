from streaming_linear_equation_solver import Solver, Const

sv = Solver()

# input: 3a - b + 4c = 15
sv.input({'a': 3, 'b': -1, 'c': 4}, 15)
print(sv.constants)
# output: {}

# input: 9a + 2c = 6
sv.input({'a': 9, 'c': 2}, 6)
print(sv.constants)
# output: {}

# input: 9a + 2c = 7, linear dependent with the equations got so far, ignored
sv.input({'a': 9, 'c': 2}, 7)
print(sv.constants)
# output: {}

# input: 5a + 3d = 5
sv.input({'a': 5, 'd': 3}, 5)
print(sv.constants)
# output: {}

# input: 8b + 9c = 7
sv.input({'b': 8, 'c': 9}, 7)
print(sv.constants)
# output: {'c': 333/107, 'b': -281/107, 'd': 1645/963, 'a': -8/321}

# input: (9/3)c + 2e = 3
sv.input({'c': Const(9, 3), 'e': 2}, 3)
print(sv.constants)
# output: {'c': 333/107, 'b': -281/107, 'd': 1645/963, 'a': -8/321, 'e': -339/107}
