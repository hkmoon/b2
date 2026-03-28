# This file is part of Bertini 2.
#
# python/test/parse_extended_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/parse_extended_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/parse_extended_test.py.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright(C) 2016-2025 by Bertini2 Development Team
#
#  See <http://www.gnu.org/licenses/> for a copy of the license,
#  as well as COPYING.  Bertini2 is provided with permitted
#  additional terms in the b2/licenses/ directory.


from bertini import *
import bertini as pb
import bertini.parse as pp
import bertini.multiprec as mp
from bertini.multiprec import Float as mpfr_float
from bertini.multiprec import Complex as mpfr_complex
import unittest
import numpy as np


class ParseSingleVariableTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-15;

    def test_parse_univariate_polynomial(self):
        sys = pp.system('function f; variable_group x; f = x^3 - 1;');
        vals = np.array([complex(2.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 7.0), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag), self.tol_d)

    def test_parse_univariate_quadratic(self):
        sys = pp.system('function f; variable_group x; f = x^2 - 4;');
        vals = np.array([complex(2.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag), self.tol_d)

    def test_parse_univariate_with_constant(self):
        sys = pp.system('function f; variable_group x; f = 3*x + 5;');
        vals = np.array([complex(1.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 8.0), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag), self.tol_d)


class ParseTwoVariableTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-15;

    def test_parse_two_functions_two_vars(self):
        sys = pp.system('function f, g; variable_group x, y; f = x + y; g = x - y;');
        vals = np.array([complex(3.0, 0.0), complex(1.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 4.0), self.tol_d)
        self.assertLessEqual(np.abs(result[1].real - 2.0), self.tol_d)

    def test_parse_circle_and_line(self):
        sys = pp.system('function f, g; variable_group x, y; f = x^2 + y^2 - 1; g = y - x;');
        vals = np.array([complex(0.0, 0.0), complex(0.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - (-1.0)), self.tol_d)
        self.assertLessEqual(np.abs(result[1].real), self.tol_d)

    def test_parse_product_terms(self):
        sys = pp.system('function f, g; variable_group x, y; f = x*y - 6; g = x^2 + y^2 - 13;');
        vals = np.array([complex(2.0, 0.0), complex(3.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real), self.tol_d)
        self.assertLessEqual(np.abs(result[1].real), self.tol_d)


class ParseThreeVariableTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-15;

    def test_parse_three_var_linear(self):
        sys = pp.system('function f, g, h; variable_group x, y, z; f = x + y + z - 6; g = x - y + z - 2; h = 2*x + y - z - 1;');
        vals = np.array([complex(1.0, 0.0), complex(2.0, 0.0), complex(3.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real), self.tol_d)
        self.assertLessEqual(np.abs(result[1].real), self.tol_d)
        self.assertLessEqual(np.abs(result[2].real), self.tol_d)

    def test_parse_three_var_mixed_degree(self):
        input_str = 'function f, g, h; variable_group x, y, z; f = x*y*z; g = x^2 + y^2 + z^2; h = x + y + z;';
        sys = pp.system(input_str);
        vals = np.array([complex(1.0, 0.0), complex(1.0, 0.0), complex(1.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 1.0), self.tol_d)
        self.assertLessEqual(np.abs(result[1].real - 3.0), self.tol_d)
        self.assertLessEqual(np.abs(result[2].real - 3.0), self.tol_d)


class ParseComplexValuesTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-14;

    def test_parse_eval_complex_point(self):
        sys = pp.system('function f; variable_group x; f = x^2;');
        vals = np.array([complex(0.0, 1.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - (-1.0)), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag), self.tol_d)

    def test_parse_eval_complex_coefficients(self):
        sys = pp.system('function f; variable_group x; f = (3 + 2*I)*x;');
        vals = np.array([complex(1.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real - 3.0), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag - 2.0), self.tol_d)


class ParseSpecialNumbersTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-10;

    def test_parse_with_pi(self):
        sys = pp.system('function f; variable_group x; f = x - pi;');
        vals = np.array([complex(np.pi, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real), self.tol_d)

    def test_parse_with_imaginary_unit(self):
        sys = pp.system('function f; variable_group x; f = I*x;');
        vals = np.array([complex(1.0, 0.0)])
        result = sys.eval(vals);
        self.assertLessEqual(np.abs(result[0].real), self.tol_d)
        self.assertLessEqual(np.abs(result[0].imag - 1.0), self.tol_d)


class ParseMalformedInputTest(unittest.TestCase):
    def test_parse_empty_string(self):
        with self.assertRaises(Exception):
            pp.system('');

    def test_parse_missing_semicolon(self):
        with self.assertRaises(Exception):
            pp.system('function f variable_group x f = x^2');

    def test_parse_missing_variable_group(self):
        with self.assertRaises(Exception):
            pp.system('function f; f = x^2;');

    def test_parse_missing_function_declaration(self):
        with self.assertRaises(Exception):
            pp.system('variable_group x; f = x^2;');


class ParseDifferentiateTest(unittest.TestCase):
    def setUp(self):
        self.tol_d = 1e-14;

    def test_parse_and_differentiate(self):
        sys = pp.system('function f; variable_group x; f = x^3;');
        sys.differentiate();
        vals = np.array([complex(2.0, 0.0)])
        jac = sys.eval_jacobian(vals);
        self.assertLessEqual(np.abs(jac[0][0].real - 12.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[0][0].imag), self.tol_d)

    def test_parse_and_differentiate_two_var(self):
        sys = pp.system('function f, g; variable_group x, y; f = x*y; g = x^2 + y^2;');
        sys.differentiate();
        vals = np.array([complex(3.0, 0.0), complex(4.0, 0.0)])
        jac = sys.eval_jacobian(vals);
        # df/dx = y = 4, df/dy = x = 3
        self.assertLessEqual(np.abs(jac[0][0].real - 4.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[0][1].real - 3.0), self.tol_d)
        # dg/dx = 2x = 6, dg/dy = 2y = 8
        self.assertLessEqual(np.abs(jac[1][0].real - 6.0), self.tol_d)
        self.assertLessEqual(np.abs(jac[1][1].real - 8.0), self.tol_d)


class ParseMultiprecisionTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float('1e-27');

    def test_parse_eval_multiprecision(self):
        sys = pp.system('function f; variable_group x; f = x^2 - 2;');
        val = np.array([mpfr_complex('1.4142135623730950488016887242097', '0')])
        result = sys.eval(val);
        self.assertLessEqual(mp.abs(result[0].real), self.tol)

    def test_parse_eval_multiprecision_two_var(self):
        sys = pp.system('function f, g; variable_group x, y; f = x + y - 1; g = x - y;');
        val = np.array([mpfr_complex('0.5', '0'), mpfr_complex('0.5', '0')])
        result = sys.eval(val);
        self.assertLessEqual(mp.abs(result[0].real), self.tol)
        self.assertLessEqual(mp.abs(result[1].real), self.tol)


class ParseDegreesTest(unittest.TestCase):
    def test_parse_system_degrees(self):
        sys = pp.system('function f, g; variable_group x, y; f = x^3 + y; g = x*y + 1;');
        degs = sys.degrees();
        self.assertEqual(degs[0], 3)
        self.assertEqual(degs[1], 2)

    def test_parse_linear_system_degrees(self):
        sys = pp.system('function f, g; variable_group x, y; f = x + y + 1; g = 2*x - y;');
        degs = sys.degrees();
        self.assertEqual(degs[0], 1)
        self.assertEqual(degs[1], 1)


if __name__ == '__main__':
    unittest.main();
