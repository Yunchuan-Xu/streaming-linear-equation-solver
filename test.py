from streaming_linear_equation_solver import Solver, Const

sv = Solver()
sv.input({'a': 3, 'b': 1, 'c': 4}, 15)
sv.input({'a': 9, 'c': 2}, 6)
sv.input({'a': 9, 'c': 2}, 7)
sv.input({'a': 5, 'd': 3}, 5)
sv.input({'b': 8, 'c': 9}, 7)
sv.input({'c': Const(9, 3), 'e': 2}, 3)    # Const(9, 3) means 9/3
