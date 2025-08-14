import bertini as pb

x = pb.Variable('x')
y = pb.Variable('y')

sys = pb.System()

sys.add_function(x-y)
sys.add_function(x**2 + y**2 - 1)

sys.add_variable_group(pb.VariableGroup([x,y]))
sys.homogenize()
sys.auto_patch()

solver = pb.nag_algorithm.ZeroDimCauchyAdaptivePrecisionTotalDegree(sys)
solver.solve()

for soln in solver.solutions():
	print(sys.dehomogenize_point(soln))