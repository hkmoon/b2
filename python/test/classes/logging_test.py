# This file is part of Bertini 2.
#
# python/test/classes/logging_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/classes/logging_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/classes/logging_test.py.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright(C) 2016-2025 by Bertini2 Development Team
#
#  See <http://www.gnu.org/licenses/> for a copy of the license,
#  as well as COPYING.  Bertini2 is provided with permitted
#  additional terms in the b2/licenses/ directory.


import unittest
import tempfile
import os

try:
    import bertini.logging as blog
    _IMPORT_OK = True
except ImportError:
    _IMPORT_OK = False


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class SeverityLevelTest(unittest.TestCase):
    def test_severity_levels_exist(self):
        self.assertIsNotNone(blog.severity_level.Debug)
        self.assertIsNotNone(blog.severity_level.Trace)
        self.assertIsNotNone(blog.severity_level.Info)
        self.assertIsNotNone(blog.severity_level.Warning)
        self.assertIsNotNone(blog.severity_level.Error)
        self.assertIsNotNone(blog.severity_level.Fatal)

    def test_severity_levels_are_distinct(self):
        levels = [
            blog.severity_level.Debug,
            blog.severity_level.Trace,
            blog.severity_level.Info,
            blog.severity_level.Warning,
            blog.severity_level.Error,
            blog.severity_level.Fatal,
        ]
        # all levels should be unique values
        self.assertEqual(len(set(int(l) for l in levels)), 6)

    def test_severity_level_ordering(self):
        self.assertLess(int(blog.severity_level.Debug), int(blog.severity_level.Fatal))


@unittest.skipUnless(_IMPORT_OK, "bertini C++ extension not available")
class LoggingFunctionsTest(unittest.TestCase):
    def test_init_callable(self):
        self.assertTrue(callable(blog.init))

    def test_set_level_callable(self):
        self.assertTrue(callable(blog.set_level))

    def test_add_file_callable(self):
        self.assertTrue(callable(blog.add_file))

    def test_init_with_defaults(self):
        # init should accept being called with defaults
        blog.init()

    def test_init_with_custom_level(self):
        blog.init(level=blog.severity_level.Debug)

    def test_set_level(self):
        blog.init()
        blog.set_level(blog.severity_level.Warning)
        blog.set_level(blog.severity_level.Debug)

    def test_init_with_custom_pattern(self):
        tmpdir = tempfile.mkdtemp()
        pattern = os.path.join(tmpdir, "test_%N.log")
        blog.init(pattern=pattern, format="%Message%", rotation_size=1024*1024, level=blog.severity_level.Info)


if __name__ == '__main__':
    unittest.main()
