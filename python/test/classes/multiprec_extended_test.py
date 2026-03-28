# This file is part of Bertini 2.
#
# python/test/multiprec_extended_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/multiprec_extended_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/multiprec_extended_test.py.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright(C) 2016-2025 by Bertini2 Development Team
#
#  See <http://www.gnu.org/licenses/> for a copy of the license,
#  as well as COPYING.  Bertini2 is provided with permitted
#  additional terms in the b2/licenses/ directory.


import bertini as pb
import bertini.multiprec as mp
from bertini.multiprec import Float as mpfr_float
from bertini.multiprec import Complex as mpfr_complex
import unittest
import numpy as np


class FloatPrecisionTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);

    def test_default_precision_set_get(self):
        mp.default_precision(30);
        x = mpfr_float("1.0");
        self.assertIsNotNone(x)

    def test_precision_30(self):
        mp.default_precision(30);
        tol = mpfr_float("1e-27");
        x = mpfr_float("3.141592653589793238462643383279");
        y = mpfr_float("3.141592653589793238462643383279");
        self.assertLessEqual(mp.abs(x - y), tol)

    def test_precision_40(self):
        mp.default_precision(40);
        tol = mpfr_float("1e-37");
        x = mpfr_float("2.718281828459045235360287471352662497757");
        one = mpfr_float("1");
        result = mp.exp(one);
        self.assertLessEqual(mp.abs(result - x), tol)
        mp.default_precision(30);

    def test_precision_50(self):
        mp.default_precision(50);
        tol = mpfr_float("1e-47");
        x = mpfr_float("1.4142135623730950488016887242096980785696718753769");
        two = mpfr_float("2");
        result = mp.sqrt(two);
        self.assertLessEqual(mp.abs(result - x), tol)
        mp.default_precision(30);

    def test_change_precision_preserves_value(self):
        mp.default_precision(30);
        x = mpfr_float("1.5");
        mp.default_precision(50);
        y = mpfr_float("1.5");
        mp.default_precision(60);
        tol = mpfr_float("1e-27");
        self.assertLessEqual(mp.abs(x - y), tol)
        mp.default_precision(30);


class FloatArithmeticExtendedTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_add_subtract_identity(self):
        x = mpfr_float("7.5");
        zero = mpfr_float("0");
        self.assertLessEqual(mp.abs((x + zero) - x), self.tol)
        self.assertLessEqual(mp.abs((x - zero) - x), self.tol)

    def test_multiply_by_one(self):
        x = mpfr_float("3.14");
        one = mpfr_float("1");
        self.assertLessEqual(mp.abs((x * one) - x), self.tol)

    def test_divide_by_self(self):
        x = mpfr_float("3.14");
        one = mpfr_float("1");
        self.assertLessEqual(mp.abs((x / x) - one), self.tol)

    def test_negation(self):
        x = mpfr_float("5.5");
        self.assertLessEqual(mp.abs((-x) + x), self.tol)

    def test_power_square(self):
        x = mpfr_float("3");
        result = x**2;
        self.assertLessEqual(mp.abs(result - mpfr_float("9")), self.tol)

    def test_power_cube(self):
        x = mpfr_float("2");
        result = x**3;
        self.assertLessEqual(mp.abs(result - mpfr_float("8")), self.tol)

    def test_repeated_operations(self):
        x = mpfr_float("1");
        for i in range(10):
            x = x + mpfr_float("1");
        self.assertLessEqual(mp.abs(x - mpfr_float("11")), self.tol)


class FloatTranscendentalExtendedTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_exp_log_inverse(self):
        x = mpfr_float("2.5");
        result = mp.log(mp.exp(x));
        self.assertLessEqual(mp.abs(result - x), self.tol)

    def test_sin_squared_plus_cos_squared(self):
        x = mpfr_float("1.23");
        s = mp.sin(x);
        c = mp.cos(x);
        result = s*s + c*c;
        self.assertLessEqual(mp.abs(result - mpfr_float("1")), self.tol)

    def test_sqrt_squared(self):
        x = mpfr_float("7.0");
        result = mp.sqrt(x);
        self.assertLessEqual(mp.abs(result * result - x), self.tol)

    def test_exp_zero(self):
        zero = mpfr_float("0");
        result = mp.exp(zero);
        self.assertLessEqual(mp.abs(result - mpfr_float("1")), self.tol)

    def test_log_one(self):
        one = mpfr_float("1");
        result = mp.log(one);
        self.assertLessEqual(mp.abs(result), self.tol)

    def test_tan_equals_sin_over_cos(self):
        x = mpfr_float("0.75");
        t = mp.tan(x);
        sc = mp.sin(x) / mp.cos(x);
        self.assertLessEqual(mp.abs(t - sc), self.tol)


class ComplexArithmeticExtendedTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_complex_add_subtract_inverse(self):
        x = mpfr_complex("3.5", "2.1");
        y = mpfr_complex("1.2", "-0.8");
        result = (x + y) - y;
        self.assertLessEqual(mp.abs(result.real - x.real), self.tol)
        self.assertLessEqual(mp.abs(result.imag - x.imag), self.tol)

    def test_complex_multiply_divide_inverse(self):
        x = mpfr_complex("3.5", "2.1");
        y = mpfr_complex("1.2", "-0.8");
        result = (x * y) / y;
        self.assertLessEqual(mp.abs(result.real - x.real), self.tol)
        self.assertLessEqual(mp.abs(result.imag - x.imag), self.tol)

    def test_complex_multiply_conjugate(self):
        a = mpfr_float("3.5");
        b = mpfr_float("2.1");
        x = mpfr_complex("3.5", "2.1");
        y = mpfr_complex("3.5", "-2.1");
        result = mpfr_complex(x * y);
        expected_real = a*a + b*b;
        self.assertLessEqual(mp.abs(result.real - expected_real), self.tol)
        self.assertLessEqual(mp.abs(result.imag), self.tol)

    def test_complex_i_squared(self):
        i = mpfr_complex("0", "1");
        result = mpfr_complex(i * i);
        self.assertLessEqual(mp.abs(result.real - mpfr_float("-1")), self.tol)
        self.assertLessEqual(mp.abs(result.imag), self.tol)

    def test_complex_negation(self):
        x = mpfr_complex("3.5", "2.1");
        neg = mpfr_complex(-x);
        self.assertLessEqual(mp.abs(neg.real - mpfr_float("-3.5")), self.tol)
        self.assertLessEqual(mp.abs(neg.imag - mpfr_float("-2.1")), self.tol)

    def test_complex_power_integer(self):
        x = mpfr_complex("1", "1");
        result = mpfr_complex(x**2);
        self.assertLessEqual(mp.abs(result.real), self.tol)
        self.assertLessEqual(mp.abs(result.imag - mpfr_float("2")), self.tol)


class ComplexPrecisionTest(unittest.TestCase):
    def test_complex_precision_tracking(self):
        mp.default_precision(30);
        x = mpfr_complex("1", "0");
        self.assertEqual(x.precision(), 30)

    def test_complex_precision_after_change(self):
        mp.default_precision(30);
        x = mpfr_complex("1", "0");
        mp.default_precision(50);
        y = mpfr_complex("2", "0");
        self.assertEqual(x.precision(), 30)
        self.assertEqual(y.precision(), 50)
        mp.default_precision(30);

    def test_complex_precision_propagation_addition(self):
        mp.default_precision(30);
        x = mpfr_complex("1", "0");
        mp.default_precision(50);
        y = mpfr_complex("2", "0");
        mp.default_precision(60);
        w = x + y;
        self.assertEqual(w.precision(), 60)
        mp.default_precision(30);

    def test_complex_precision_propagation_multiplication(self):
        mp.default_precision(30);
        x = mpfr_complex("2", "1");
        mp.default_precision(50);
        y = mpfr_complex("3", "-1");
        mp.default_precision(60);
        w = x * y;
        self.assertEqual(w.precision(), 60)
        mp.default_precision(30);

    def test_complex_assignment_preserves_source_precision(self):
        mp.default_precision(40);
        a = mpfr_complex("4", "0");
        mp.default_precision(60);
        b = a;
        self.assertEqual(b.precision(), 40)
        mp.default_precision(30);


class ComplexTranscendentalExtendedTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_complex_exp_log_inverse(self):
        x = mpfr_complex("1.5", "0.7");
        result = mp.log(mp.exp(x));
        self.assertLessEqual(mp.abs(result.real - x.real), self.tol)
        self.assertLessEqual(mp.abs(result.imag - x.imag), self.tol)

    def test_complex_sin_squared_plus_cos_squared(self):
        x = mpfr_complex("1.5", "0.7");
        s = mp.sin(x);
        c = mp.cos(x);
        result = mpfr_complex(s*s + c*c);
        self.assertLessEqual(mp.abs(result.real - mpfr_float("1")), self.tol)
        self.assertLessEqual(mp.abs(result.imag), self.tol)

    def test_complex_sqrt(self):
        x = mpfr_complex("3", "4");
        result = mp.sqrt(x);
        squared = mpfr_complex(result * result);
        self.assertLessEqual(mp.abs(squared.real - x.real), self.tol)
        self.assertLessEqual(mp.abs(squared.imag - x.imag), self.tol)

    def test_complex_abs(self):
        x = mpfr_complex("3", "4");
        result = mp.abs(x);
        self.assertLessEqual(mp.abs(result - mpfr_float("5")), self.tol)


class ComplexConstructionTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_construct_from_int(self):
        x = mpfr_complex(3);
        self.assertLessEqual(mp.abs(x.real - mpfr_float("3")), self.tol)
        self.assertLessEqual(mp.abs(x.imag), self.tol)

    def test_construct_from_float(self):
        x = mpfr_complex(3.5);
        self.assertLessEqual(mp.abs(x.real - mpfr_float("3.5")), self.tol)

    def test_construct_from_mpfr_float(self):
        f = mpfr_float("2.718");
        x = mpfr_complex(f);
        self.assertLessEqual(mp.abs(x.real - f), self.tol)

    def test_construct_from_string(self):
        x = mpfr_complex("5.5");
        self.assertLessEqual(mp.abs(x.real - mpfr_float("5.5")), self.tol)

    def test_construct_from_two_strings(self):
        x = mpfr_complex("3.5", "2.1");
        self.assertLessEqual(mp.abs(x.real - mpfr_float("3.5")), self.tol)
        self.assertLessEqual(mp.abs(x.imag - mpfr_float("2.1")), self.tol)

    def test_construct_from_two_floats(self):
        x = mpfr_complex(3.5, 2.1);
        self.assertLessEqual(mp.abs(x.real - mpfr_float("3.5")), self.tol)

    def test_construct_from_two_mpfr_floats(self):
        r = mpfr_float("2.98");
        i = mpfr_float("-1e-4");
        x = mpfr_complex(r, i);
        self.assertLessEqual(mp.abs(x.real - r), self.tol)
        self.assertLessEqual(mp.abs(x.imag - i), self.tol)

    def test_construct_from_mixed_types(self):
        x = mpfr_complex("6e2", mpfr_float("4.32"));
        self.assertLessEqual(mp.abs(x.real - mpfr_float("600")), self.tol)
        self.assertLessEqual(mp.abs(x.imag - mpfr_float("4.32")), self.tol)

    def test_copy_construction(self):
        x = mpfr_complex("3.5", "2.1");
        y = mpfr_complex(x);
        self.assertLessEqual(mp.abs(y.real - x.real), self.tol)
        self.assertLessEqual(mp.abs(y.imag - x.imag), self.tol)


class ComplexPolarTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_polar_construction(self):
        r = mpfr_float("5");
        theta = mpfr_float("0");
        result = mp.polar(r, theta);
        self.assertLessEqual(mp.abs(result.real - mpfr_float("5")), self.tol)
        self.assertLessEqual(mp.abs(result.imag), self.tol)

    def test_polar_quarter_turn(self):
        r = mpfr_float("1");
        theta = mp.acos(mpfr_float("-1")) / 2;  # pi/2
        result = mp.polar(r, theta);
        self.assertLessEqual(mp.abs(result.real), self.tol)
        self.assertLessEqual(mp.abs(result.imag - mpfr_float("1")), self.tol)

    def test_arg_roundtrip(self):
        x = mpfr_complex("3", "4");
        r = mp.abs(x);
        theta = mp.arg(x);
        reconstructed = mp.polar(r, theta);
        self.assertLessEqual(mp.abs(reconstructed.real - x.real), self.tol)
        self.assertLessEqual(mp.abs(reconstructed.imag - x.imag), self.tol)


class VectorTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_vector_creation(self):
        v = mp.Vector(3);
        self.assertEqual(len(v), 3)

    def test_vector_zero_init(self):
        v = mp.Vector(2);
        self.assertLessEqual(mp.abs(v[0].real), self.tol)
        self.assertLessEqual(mp.abs(v[0].imag), self.tol)

    def test_vector_assignment(self):
        v = mp.Vector(2);
        v[0] = mpfr_complex("3.5", "2.1");
        v[1] = mpfr_complex("1.2", "-0.8");
        self.assertLessEqual(mp.abs(v[0].real - mpfr_float("3.5")), self.tol)
        self.assertLessEqual(mp.abs(v[1].imag - mpfr_float("-0.8")), self.tol)

    def test_vector_empty(self):
        v = mp.Vector(0);
        self.assertEqual(len(v), 0)

    def test_vector_in_system_eval(self):
        sys = pb.parse.system('function f; variable_group x; f = x^2;');
        v = mp.Vector(1);
        v[0] = mpfr_complex("3", "0");
        result = sys.eval(v);
        self.assertLessEqual(mp.abs(result[0].real - mpfr_float("9")), self.tol)


class FloatComparisonTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30);
        self.tol = mpfr_float("1e-27");

    def test_abs_positive(self):
        x = mpfr_float("5.5");
        self.assertLessEqual(mp.abs(x - mpfr_float("5.5")), self.tol)

    def test_abs_negative(self):
        x = mpfr_float("-5.5");
        result = mp.abs(x);
        self.assertLessEqual(mp.abs(result - mpfr_float("5.5")), self.tol)

    def test_abs_zero(self):
        x = mpfr_float("0");
        result = mp.abs(x);
        self.assertLessEqual(result, self.tol)


class HighPrecisionComputationTest(unittest.TestCase):
    def test_high_precision_exp(self):
        mp.default_precision(60);
        tol = mpfr_float("1e-55");
        one = mpfr_float("1");
        e = mp.exp(one);
        log_e = mp.log(e);
        self.assertLessEqual(mp.abs(log_e - one), tol)
        mp.default_precision(30);

    def test_high_precision_trig(self):
        mp.default_precision(60);
        tol = mpfr_float("1e-55");
        x = mpfr_float("0.5");
        identity = mp.sin(x)**2 + mp.cos(x)**2;
        self.assertLessEqual(mp.abs(identity - mpfr_float("1")), tol)
        mp.default_precision(30);

    def test_high_precision_complex_arithmetic(self):
        mp.default_precision(60);
        tol = mpfr_float("1e-55");
        x = mpfr_complex("1.23456789012345678901234567890", "0.98765432109876543210987654321");
        result = mpfr_complex(x * mpfr_complex("1", "0"));
        self.assertLessEqual(mp.abs(result.real - x.real), tol)
        self.assertLessEqual(mp.abs(result.imag - x.imag), tol)
        mp.default_precision(30);


if __name__ == '__main__':
    unittest.main();
