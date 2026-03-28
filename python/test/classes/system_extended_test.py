# This file is part of Bertini 2.
#
# python/test/system_extended_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/system_extended_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/system_extended_test.py.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright(C) 2016-2025 by Bertini2 Development Team
#
#  See <http://www.gnu.org/licenses/> for a copy of the license,
#  as well as COPYING.  Bertini2 is provided with permitted
#  additional terms in the b2/licenses/ directory.


from bertini import *
from bertini.function_tree.symbol import *
from bertini.function_tree.root import *
from bertini.function_tree import *
import bertini as pb
import bertini.multiprec as mp
from bertini.multiprec import Float as mpfr_float
from bertini.multiprec import Complex as mpfr_complex
import unittest
import numpy as np


class SystemCreationTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-15;

    def test_create_empty_system(self):
        s = System();
        self.assertIsNotNone(s)

    def test_create_single_var_system(self):
        x = Variable("x");
        f = Function(x**2);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        s.add_variable_group(vg)
        s.add_function(f)
        vals = np.array([complex(3.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 9.0), self.tol_d)

    def test_create_two_var_system(self):
        x = Variable("x");
        y = Variable("y");
        f = Function(x + y);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(f)
        vals = np.array([complex(2.0, 0.0), complex(3.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 5.0), self.tol_d)

    def test_create_three_var_system(self):
        x = Variable("x");
        y = Variable("y");
        z = Variable("z");
        f = Function(x*y*z);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        vg.append(z)
        s.add_variable_group(vg)
        s.add_function(f)
        vals = np.array([complex(2.0, 0.0), complex(3.0, 0.0), complex(4.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 24.0), self.tol_d)


class SystemFunctionManagementTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-15;

    def test_add_multiple_functions(self):
        x = Variable("x");
        y = Variable("y");
        f1 = Function(x + y);
        f2 = Function(x * y);
        f3 = Function(x**2 + y**2);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(f1)
        s.add_function(f2)
        s.add_function(f3)
        vals = np.array([complex(1.0, 0.0), complex(2.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 3.0), self.tol_d)
        self.assertLessEqual(np.abs(result[1].real - 2.0), self.tol_d)
        self.assertLessEqual(np.abs(result[2].real - 5.0), self.tol_d)

    def test_add_function_expression(self):
        x = Variable("x");
        y = Variable("y");
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(x + y)
        vals = np.array([complex(4.0, 0.0), complex(5.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 9.0), self.tol_d)

    def test_add_function_with_constant(self):
        x = Variable("x");
        a = Float("2.5", "0");
        f = Function(a * x);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        s.add_variable_group(vg)
        s.add_function(f)
        vals = np.array([complex(4.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 10.0), self.tol_d)


class SystemEvalTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-14;

    def test_eval_at_origin(self):
        x = Variable("x");
        y = Variable("y");
        f = Function(x**2 + y**2 - 1);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(f)
        vals = np.array([complex(0.0, 0.0), complex(0.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - (-1.0)), self.tol_d)

    def test_eval_at_complex_point(self):
        x = Variable("x");
        f = Function(x**2);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        s.add_variable_group(vg)
        s.add_function(f)
        vals = np.array([complex(1.0, 1.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 0.0), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag - 2.0), self.tol_d)

    def test_eval_multiprec(self):
        mp.default_precision(30);
        tol = mpfr_float('1e-27');
        sys = pb.parse.system('function f; variable_group x; f = x^2 + 1;');
        vals = np.array([mpfr_complex('0', '1')])
        result = sys.eval(vals);
        self.assertLessEqual(mp.abs(result[0].real), tol)
        self.assertLessEqual(mp.abs(result[0].imag), tol)

    def test_eval_known_values(self):
        x = Variable("x");
        y = Variable("y");
        a = Float("4.897", "1.23");
        f = Function(x*y);
        g = Function(pow(x, 2)*y - a*x);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(f)
        s.add_function(g)
        vals = np.array([complex(3.5, 2.89), complex(-9.32, 0.0765)])
        result = s.eval(vals);
        # x*y = (3.5 + 2.89i)*(-9.32 + 0.0765i) = (-32.841085) + (-26.66705)i
        self.assertLessEqual(np.abs(result[0].real / (-32.841085) - 1), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag / (-26.66705) - 1), self.tol_d)


class SystemJacobianTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-14;

    def test_jacobian_linear(self):
        x = Variable("x");
        y = Variable("y");
        f1 = Function(2*x + 3*y);
        f2 = Function(x - y);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(f1)
        s.add_function(f2)
        s.differentiate();
        vals = np.array([complex(1.0, 0.0), complex(1.0, 0.0)])
        jac = s.eval_jacobian(vals);
        self.assertLessEqual(np.abs(jac[0][0].real - 2.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[0][1].real - 3.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[1][0].real - 1.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[1][1].real - (-1.0)), self.tol_d)

    def test_jacobian_quadratic(self):
        x = Variable("x");
        y = Variable("y");
        f1 = Function(x**2 + y**2);
        f2 = Function(x*y);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(f1)
        s.add_function(f2)
        s.differentiate();
        vals = np.array([complex(3.0, 0.0), complex(4.0, 0.0)])
        jac = s.eval_jacobian(vals);
        # df1/dx = 2x = 6, df1/dy = 2y = 8
        self.assertLessEqual(np.abs(jac[0][0].real - 6.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[0][1].real - 8.0), self.tol_d)
        # df2/dx = y = 4, df2/dy = x = 3
        self.assertLessEqual(np.abs(jac[1][0].real - 4.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[1][1].real - 3.0), self.tol_d)

    def test_jacobian_three_var(self):
        x = Variable("x");
        y = Variable("y");
        z = Variable("z");
        f = Function(x*y*z);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        vg.append(z)
        s.add_variable_group(vg)
        s.add_function(f)
        s.differentiate();
        vals = np.array([complex(2.0, 0.0), complex(3.0, 0.0), complex(5.0, 0.0)])
        jac = s.eval_jacobian(vals);
        # df/dx = yz = 15, df/dy = xz = 10, df/dz = xy = 6
        self.assertLessEqual(np.abs(jac[0][0].real - 15.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[0][1].real - 10.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[0][2].real - 6.0), self.tol_d)

    def test_jacobian_multiprec(self):
        mp.default_precision(30);
        tol = mpfr_float('1e-27');
        sys = pb.parse.system('function f, g; variable_group x, y; f = x^2; g = y^2;');
        sys.differentiate();
        vals = np.array([mpfr_complex('3', '0'), mpfr_complex('4', '0')])
        jac = sys.eval_jacobian(vals);
        self.assertLessEqual(mp.abs(jac[0][0].real / mpfr_float('6') - 1), tol)
        self.assertLessEqual(mp.abs(jac[1][1].real / mpfr_float('8') - 1), tol)
        self.assertLessEqual(mp.abs(jac[0][1].real), tol)
        self.assertLessEqual(mp.abs(jac[1][0].real), tol)


class SystemDegreeTest(unittest.TestCase):
    def test_degree_linear(self):
        x = Variable("x");
        y = Variable("y");
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(x + y + 1)
        degs = s.degrees();
        self.assertEqual(degs[0], 1)

    def test_degree_quadratic(self):
        x = Variable("x");
        y = Variable("y");
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(x**2 + y**2 - 1)
        degs = s.degrees();
        self.assertEqual(degs[0], 2)

    def test_degree_cubic(self):
        x = Variable("x");
        y = Variable("y");
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(x**3 + y)
        degs = s.degrees();
        self.assertEqual(degs[0], 3)

    def test_degree_mixed_system(self):
        x = Variable("x");
        y = Variable("y");
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s.add_variable_group(vg)
        s.add_function(x**3 + y)
        s.add_function(x*y)
        degs = s.degrees();
        self.assertEqual(degs[0], 3)
        self.assertEqual(degs[1], 2)

    def test_degree_from_parsed_system(self):
        sys = pb.parse.system('function f, g; variable_group x, y; f = x^4 + y^2; g = x*y^3;');
        degs = sys.degrees();
        self.assertEqual(degs[0], 4)
        self.assertEqual(degs[1], 4)


class SystemVariableGroupTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-15;

    def test_variable_group_append(self):
        vg = pb.VariableGroup()
        x = Variable("x");
        y = Variable("y");
        vg.append(x)
        vg.append(y)
        s = System();
        s.add_variable_group(vg)
        s.add_function(x + y)
        vals = np.array([complex(1.0, 0.0), complex(2.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 3.0), self.tol_d)

    def test_variable_group_str(self):
        vg = pb.VariableGroup()
        x = Variable("x");
        y = Variable("y");
        vg.append(x)
        vg.append(y)
        s = str(vg)
        self.assertIn('x', s)
        self.assertIn('y', s)


class SystemAdditionTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-15;

    def test_add_systems_cancel(self):
        x = Variable("x");
        y = Variable("y");
        s1 = System();
        s2 = System();
        vg = pb.VariableGroup()
        vg.append(x)
        vg.append(y)
        s1.add_variable_group(vg)
        s1.add_function(x + y)
        s2.add_variable_group(vg)
        s2.add_function(-x - y)
        s1 += s2;
        vals = np.array([complex(5.0, 0.0), complex(7.0, 0.0)])
        result = s1.eval(vals);
        self.assertLessEqual(np.abs(result[0].real), self.tol_d)

    def test_mult_system_by_integer(self):
        x = Variable("x");
        f = Function(x + 1);
        s = System();
        vg = pb.VariableGroup()
        vg.append(x)
        s.add_variable_group(vg)
        s.add_function(f)
        s *= Integer(3);
        vals = np.array([complex(2.0, 0.0)])
        result = s.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 9.0), self.tol_d)


class SystemStartSystemTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-14;

    def test_total_degree_start_system(self):
        sys = pb.parse.system('function f, g; variable_group x, y; f = x^2 + y; g = x + y^2;');
        td = pb.system.start_system.TotalDegree(sys);
        self.assertIsNotNone(td)
        num_start = td.num_start_points();
        degs = sys.degrees();
        expected = 1;
        for d in degs:
            expected *= d;
        self.assertEqual(num_start, expected)

    def test_total_degree_linear(self):
        sys = pb.parse.system('function f, g; variable_group x, y; f = x + y - 1; g = x - y;');
        td = pb.system.start_system.TotalDegree(sys);
        self.assertEqual(td.num_start_points(), 1)

    def test_total_degree_cubic(self):
        sys = pb.parse.system('function f, g; variable_group x, y; f = x^3 + y; g = x + y^3;');
        td = pb.system.start_system.TotalDegree(sys);
        self.assertEqual(td.num_start_points(), 9)


if __name__ == '__main__':
    unittest.main();
