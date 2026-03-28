# This file is part of Bertini 2.
#
# python/test/classes/container_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/classes/container_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/classes/container_test.py.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright(C) 2016-2025 by Bertini2 Development Team
#
#  See <http://www.gnu.org/licenses/> for a copy of the license,
#  as well as COPYING.  Bertini2 is provided with permitted
#  additional terms in the b2/licenses/ directory.


import unittest

try:
    import bertini
    from bertini.container import *
    from bertini.function_tree.symbol import Variable
    from bertini.function_tree.root import Function
    import bertini.multiprec as mp
    _IMPORT_OK = True
except ImportError:
    _IMPORT_OK = False


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class VariableGroupTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30)

    def test_create_empty(self):
        vg = VariableGroup()
        self.assertEqual(len(vg), 0)

    def test_append_variables(self):
        vg = VariableGroup()
        x = Variable("x")
        y = Variable("y")
        vg.append(x)
        vg.append(y)
        self.assertEqual(len(vg), 2)

    def test_indexing(self):
        vg = VariableGroup()
        x = Variable("x")
        y = Variable("y")
        z = Variable("z")
        vg.append(x)
        vg.append(y)
        vg.append(z)
        self.assertEqual(len(vg), 3)
        # indexing should return an element without raising
        elem = vg[0]
        self.assertIsNotNone(elem)
        elem2 = vg[2]
        self.assertIsNotNone(elem2)

    def test_str_repr(self):
        vg = VariableGroup()
        x = Variable("x")
        vg.append(x)
        s = str(vg)
        self.assertIsInstance(s, str)
        r = repr(vg)
        self.assertIsInstance(r, str)

    def test_iteration(self):
        vg = VariableGroup()
        for name in ["a", "b", "c"]:
            vg.append(Variable(name))
        count = 0
        for _ in vg:
            count += 1
        self.assertEqual(count, 3)

    def test_delete_element(self):
        vg = VariableGroup()
        vg.append(Variable("x"))
        vg.append(Variable("y"))
        self.assertEqual(len(vg), 2)
        del vg[0]
        self.assertEqual(len(vg), 1)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class ListOfIntTest(unittest.TestCase):
    def test_create_empty(self):
        li = ListOfInt()
        self.assertEqual(len(li), 0)

    def test_append_and_access(self):
        li = ListOfInt()
        li.append(42)
        li.append(-7)
        li.append(0)
        self.assertEqual(len(li), 3)
        self.assertEqual(li[0], 42)
        self.assertEqual(li[1], -7)
        self.assertEqual(li[2], 0)

    def test_delete_element(self):
        li = ListOfInt()
        li.append(1)
        li.append(2)
        li.append(3)
        del li[1]
        self.assertEqual(len(li), 2)
        self.assertEqual(li[0], 1)
        self.assertEqual(li[1], 3)

    def test_iteration(self):
        li = ListOfInt()
        values = [10, 20, 30, 40]
        for v in values:
            li.append(v)
        result = [x for x in li]
        self.assertEqual(result, values)

    def test_str_repr(self):
        li = ListOfInt()
        li.append(5)
        self.assertIsInstance(str(li), str)
        self.assertIsInstance(repr(li), str)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class ListOfFunctionTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30)

    def test_create_empty(self):
        lf = ListOfFunction()
        self.assertEqual(len(lf), 0)

    def test_append_functions(self):
        lf = ListOfFunction()
        x = Variable("x")
        y = Variable("y")
        f1 = Function(x**2 + y)
        f2 = Function(x * y - 1)
        lf.append(f1)
        lf.append(f2)
        self.assertEqual(len(lf), 2)

    def test_indexing(self):
        lf = ListOfFunction()
        x = Variable("x")
        f = Function(x**3)
        lf.append(f)
        self.assertIsNotNone(lf[0])


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class ListOfRationalTest(unittest.TestCase):
    def test_create_empty(self):
        lr = ListOfRational()
        self.assertEqual(len(lr), 0)

    def test_str_repr(self):
        lr = ListOfRational()
        self.assertIsInstance(str(lr), str)
        self.assertIsInstance(repr(lr), str)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class ListOfVariableGroupTest(unittest.TestCase):
    def setUp(self):
        mp.default_precision(30)

    def test_create_empty(self):
        lvg = ListOfVariableGroup()
        self.assertEqual(len(lvg), 0)

    def test_append_variable_groups(self):
        lvg = ListOfVariableGroup()
        vg1 = VariableGroup()
        vg1.append(Variable("x"))
        vg2 = VariableGroup()
        vg2.append(Variable("y"))
        vg2.append(Variable("z"))
        lvg.append(vg1)
        lvg.append(vg2)
        self.assertEqual(len(lvg), 2)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class ListOfVectorComplexTest(unittest.TestCase):
    def test_create_double_precision(self):
        lv = ListOfVectorComplexDoublePrecision()
        self.assertEqual(len(lv), 0)

    def test_create_variable_precision(self):
        lv = ListOfVectorComplexVariablePrecision()
        self.assertEqual(len(lv), 0)

    def test_str_repr_double(self):
        lv = ListOfVectorComplexDoublePrecision()
        self.assertIsInstance(str(lv), str)
        self.assertIsInstance(repr(lv), str)

    def test_str_repr_variable(self):
        lv = ListOfVectorComplexVariablePrecision()
        self.assertIsInstance(str(lv), str)
        self.assertIsInstance(repr(lv), str)


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class ListOfMetaDataTest(unittest.TestCase):
    def test_create_solution_metadata_double(self):
        ls = ListOfSolutionMetaData_DoublePrec()
        self.assertEqual(len(ls), 0)

    def test_create_solution_metadata_multi(self):
        ls = ListOfSolutionMetaData_MultiPrec()
        self.assertEqual(len(ls), 0)

    def test_create_eg_boundary_double(self):
        le = ListOfEGBoundaryMetaData_DoublePrec()
        self.assertEqual(len(le), 0)

    def test_create_eg_boundary_multi(self):
        le = ListOfEGBoundaryMetaData_MultiPrec()
        self.assertEqual(len(le), 0)


if __name__ == '__main__':
    unittest.main()
