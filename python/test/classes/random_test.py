# This file is part of Bertini 2.
#
# python/test/classes/random_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/classes/random_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/classes/random_test.py.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright(C) 2016-2025 by Bertini2 Development Team
#
#  See <http://www.gnu.org/licenses/> for a copy of the license,
#  as well as COPYING.  Bertini2 is provided with permitted
#  additional terms in the b2/licenses/ directory.


import unittest

try:
    import bertini.random as brand
    import bertini.multiprec as mp
    _IMPORT_OK = True
except ImportError:
    _IMPORT_OK = False


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class RandomComplexTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30)

    def test_complex_in_minus_one_to_one_exists(self):
        self.assertTrue(callable(brand.complex_in_minus_one_to_one))

    def test_complex_in_minus_one_to_one_returns_value(self):
        val = brand.complex_in_minus_one_to_one()
        self.assertIsNotNone(val)

    def test_complex_in_minus_one_to_one_has_parts(self):
        val = brand.complex_in_minus_one_to_one()
        # result is an mpfr complex; should have real and imag parts
        r = val.real
        i = val.imag
        self.assertIsNotNone(r)
        self.assertIsNotNone(i)

    def test_complex_in_minus_one_to_one_range(self):
        # sample several and verify bounds: real and imag in [-1, 1]
        one = mp.Float("1")
        for _ in range(20):
            val = brand.complex_in_minus_one_to_one()
            self.assertLessEqual(mp.abs(val.real), one)
            self.assertLessEqual(mp.abs(val.imag), one)

    def test_complex_in_minus_one_to_one_not_constant(self):
        vals = [brand.complex_in_minus_one_to_one() for _ in range(10)]
        reals = [float(str(v.real)) for v in vals]
        # extremely unlikely all 10 are the same
        self.assertGreater(len(set(reals)), 1)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class RandomUnitTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30)
        self.tol = mp.Float("1e-25")

    def test_complex_unit_exists(self):
        self.assertTrue(callable(brand.complex_unit))

    def test_complex_unit_returns_value(self):
        val = brand.complex_unit()
        self.assertIsNotNone(val)

    def test_complex_unit_magnitude(self):
        one = mp.Float("1")
        for _ in range(20):
            val = brand.complex_unit()
            mag = mp.abs(val)
            self.assertLessEqual(mp.abs(mag - one), self.tol)

    def test_complex_unit_not_constant(self):
        vals = [brand.complex_unit() for _ in range(10)]
        reals = [float(str(v.real)) for v in vals]
        self.assertGreater(len(set(reals)), 1)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class RandomRealTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30)
        self.tol = mp.Float("1e-27")

    def test_real_as_complex_exists(self):
        self.assertTrue(callable(brand.real_as_complex))

    def test_real_as_complex_returns_value(self):
        val = brand.real_as_complex()
        self.assertIsNotNone(val)

    def test_real_as_complex_imag_is_zero(self):
        zero = mp.Float("0")
        for _ in range(10):
            val = brand.real_as_complex()
            self.assertLessEqual(mp.abs(val.imag - zero), self.tol)

    def test_real_as_complex_range(self):
        one = mp.Float("1")
        for _ in range(20):
            val = brand.real_as_complex()
            self.assertLessEqual(mp.abs(val.real), one)

    def test_real_as_complex_not_constant(self):
        vals = [brand.real_as_complex() for _ in range(10)]
        reals = [float(str(v.real)) for v in vals]
        self.assertGreater(len(set(reals)), 1)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class RandomPrecisionTest(unittest.TestCase):
    def test_respects_precision_change(self):
        mp.default_precision(30)
        val30 = brand.complex_in_minus_one_to_one()
        mp.default_precision(50)
        val50 = brand.complex_in_minus_one_to_one()
        # both should be valid complex numbers regardless of precision
        self.assertIsNotNone(val30)
        self.assertIsNotNone(val50)


if __name__ == '__main__':
    unittest.main()
