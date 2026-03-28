# This file is part of Bertini 2.
#
# python/test/tracking/observer_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/tracking/observer_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/tracking/observer_test.py.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright(C) 2016-2025 by Bertini2 Development Team
#
#  See <http://www.gnu.org/licenses/> for a copy of the license,
#  as well as COPYING.  Bertini2 is provided with permitted
#  additional terms in the b2/licenses/ directory.

#  individual authors of this file include:
#
#  silviana amethyst
#  UWEC
#  Spring 2018
#


import unittest
import numpy as np

try:
    from bertini import *
    from bertini.function_tree.symbol import *
    from bertini.function_tree.root import *
    from bertini.function_tree import *
    from bertini.tracking import *
    from bertini.tracking.config import *
    import bertini.tracking.observers.amp as amp_obs
    import bertini.tracking.observers.double as double_obs
    import bertini.tracking.observers.multiple as multiple_obs
    import bertini.multiprec as mp
    from bertini.multiprec import Float as mpfr_float
    from bertini.multiprec import Complex as mpfr_complex
    HAS_BERTINI = True
except ImportError:
    HAS_BERTINI = False


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class AMPObserverTest(unittest.TestCase):
    """Tests for AMP tracker observers."""

    def test_gory_detail_logger_exists(self):
        """GoryDetailLogger class should exist in the amp observer module."""
        self.assertTrue(hasattr(amp_obs, 'GoryDetailLogger'))

    def test_first_precision_recorder_exists(self):
        """FirstPrecisionRecorder class should exist in the amp observer module."""
        self.assertTrue(hasattr(amp_obs, 'FirstPrecisionRecorder'))

    def test_abstract_exists(self):
        """Abstract observer base class should exist in the amp observer module."""
        self.assertTrue(hasattr(amp_obs, 'Abstract'))

    def test_gory_detail_logger_instantiation(self):
        """GoryDetailLogger should be instantiable with no arguments."""
        obs = amp_obs.GoryDetailLogger()
        self.assertIsNotNone(obs)

    def test_first_precision_recorder_instantiation(self):
        """FirstPrecisionRecorder should be instantiable with no arguments."""
        obs = amp_obs.FirstPrecisionRecorder()
        self.assertIsNotNone(obs)

    def test_attach_gory_detail_logger_to_amp_tracker(self):
        """GoryDetailLogger should be attachable to an AMPTracker via add_observer."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        tracker = AMPTracker(s)
        obs = amp_obs.GoryDetailLogger()
        tracker.add_observer(obs)

    def test_attach_first_precision_recorder_to_amp_tracker(self):
        """FirstPrecisionRecorder should be attachable to an AMPTracker."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        tracker = AMPTracker(s)
        obs = amp_obs.FirstPrecisionRecorder()
        tracker.add_observer(obs)

    def test_remove_observer_from_amp_tracker(self):
        """Observers should be removable from an AMPTracker via remove_observer."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        tracker = AMPTracker(s)
        obs = amp_obs.GoryDetailLogger()
        tracker.add_observer(obs)
        tracker.remove_observer(obs)

    def test_amp_tracker_observers_attribute(self):
        """AMPTracker should have an observers attribute listing available observer types."""
        self.assertTrue(hasattr(AMPTracker, 'observers'))
        obs_list = AMPTracker.observers
        self.assertIsInstance(obs_list, list)
        self.assertIn('GoryDetailLogger', obs_list)
        self.assertIn('FirstPrecisionRecorder', obs_list)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class DoublePrecisionObserverTest(unittest.TestCase):
    """Tests for double precision tracker observers."""

    def test_gory_detail_logger_exists(self):
        """GoryDetailLogger class should exist in the double observer module."""
        self.assertTrue(hasattr(double_obs, 'GoryDetailLogger'))

    def test_abstract_exists(self):
        """Abstract observer base class should exist in the double observer module."""
        self.assertTrue(hasattr(double_obs, 'Abstract'))

    def test_gory_detail_logger_instantiation(self):
        """GoryDetailLogger should be instantiable with no arguments."""
        obs = double_obs.GoryDetailLogger()
        self.assertIsNotNone(obs)

    def test_attach_gory_detail_logger_to_double_tracker(self):
        """GoryDetailLogger should be attachable to a DoublePrecisionTracker."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        tracker = DoublePrecisionTracker(s)
        obs = double_obs.GoryDetailLogger()
        tracker.add_observer(obs)

    def test_remove_observer_from_double_tracker(self):
        """Observers should be removable from a DoublePrecisionTracker."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        tracker = DoublePrecisionTracker(s)
        obs = double_obs.GoryDetailLogger()
        tracker.add_observer(obs)
        tracker.remove_observer(obs)

    def test_double_tracker_observers_attribute(self):
        """DoublePrecisionTracker should have an observers attribute."""
        self.assertTrue(hasattr(DoublePrecisionTracker, 'observers'))
        obs_list = DoublePrecisionTracker.observers
        self.assertIsInstance(obs_list, list)
        self.assertIn('GoryDetailLogger', obs_list)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class MultiplePrecisionObserverTest(unittest.TestCase):
    """Tests for multiple precision tracker observers."""

    def test_gory_detail_logger_exists(self):
        """GoryDetailLogger class should exist in the multiple observer module."""
        self.assertTrue(hasattr(multiple_obs, 'GoryDetailLogger'))

    def test_abstract_exists(self):
        """Abstract observer base class should exist in the multiple observer module."""
        self.assertTrue(hasattr(multiple_obs, 'Abstract'))

    def test_gory_detail_logger_instantiation(self):
        """GoryDetailLogger should be instantiable with no arguments."""
        obs = multiple_obs.GoryDetailLogger()
        self.assertIsNotNone(obs)

    def test_attach_gory_detail_logger_to_multiple_tracker(self):
        """GoryDetailLogger should be attachable to a MultiplePrecisionTracker."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        tracker = MultiplePrecisionTracker(s)
        obs = multiple_obs.GoryDetailLogger()
        tracker.add_observer(obs)

    def test_remove_observer_from_multiple_tracker(self):
        """Observers should be removable from a MultiplePrecisionTracker."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        tracker = MultiplePrecisionTracker(s)
        obs = multiple_obs.GoryDetailLogger()
        tracker.add_observer(obs)
        tracker.remove_observer(obs)

    def test_multiple_tracker_observers_attribute(self):
        """MultiplePrecisionTracker should have an observers attribute."""
        self.assertTrue(hasattr(MultiplePrecisionTracker, 'observers'))
        obs_list = MultiplePrecisionTracker.observers
        self.assertIsInstance(obs_list, list)
        self.assertIn('GoryDetailLogger', obs_list)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class EndgameObserverTest(unittest.TestCase):
    """Tests for endgame observers."""

    def setUp(self):
        try:
            import bertini._pybertini.endgame.observers as eg_obs
            self.eg_obs = eg_obs
            self.has_eg_observers = True
        except (ImportError, AttributeError):
            self.has_eg_observers = False

    def test_endgame_observer_modules_exist(self):
        """Endgame observer submodules should be importable."""
        if not self.has_eg_observers:
            self.skipTest("endgame.observers not available")
        for submod_name in ['amp_cauchy', 'amp_pseg', 'double_cauchy',
                            'double_pseg', 'multiple_cauchy', 'multiple_pseg']:
            self.assertTrue(hasattr(self.eg_obs, submod_name),
                            f"Missing endgame observer submodule: {submod_name}")

    def test_amp_cauchy_gory_detail_logger(self):
        """AMP Cauchy endgame GoryDetailLogger should be instantiable."""
        if not self.has_eg_observers:
            self.skipTest("endgame.observers not available")
        mod = getattr(self.eg_obs, 'amp_cauchy', None)
        if mod is None:
            self.skipTest("amp_cauchy observers not available")
        self.assertTrue(hasattr(mod, 'GoryDetailLogger'))
        obs = mod.GoryDetailLogger()
        self.assertIsNotNone(obs)

    def test_amp_pseg_gory_detail_logger(self):
        """AMP PSEG endgame GoryDetailLogger should be instantiable."""
        if not self.has_eg_observers:
            self.skipTest("endgame.observers not available")
        mod = getattr(self.eg_obs, 'amp_pseg', None)
        if mod is None:
            self.skipTest("amp_pseg observers not available")
        self.assertTrue(hasattr(mod, 'GoryDetailLogger'))
        obs = mod.GoryDetailLogger()
        self.assertIsNotNone(obs)

    def test_double_cauchy_gory_detail_logger(self):
        """Double precision Cauchy endgame GoryDetailLogger should be instantiable."""
        if not self.has_eg_observers:
            self.skipTest("endgame.observers not available")
        mod = getattr(self.eg_obs, 'double_cauchy', None)
        if mod is None:
            self.skipTest("double_cauchy observers not available")
        self.assertTrue(hasattr(mod, 'GoryDetailLogger'))
        obs = mod.GoryDetailLogger()
        self.assertIsNotNone(obs)

    def test_attach_observer_to_amp_cauchy_endgame(self):
        """GoryDetailLogger should be attachable to an AMPCauchyEG."""
        if not self.has_eg_observers:
            self.skipTest("endgame.observers not available")
        mod = getattr(self.eg_obs, 'amp_cauchy', None)
        if mod is None:
            self.skipTest("amp_cauchy observers not available")

        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        from bertini.endgame import AMPCauchyEG
        tracker = AMPTracker(s)
        stepping = SteppingConfig()
        newton = NewtonConfig()
        tracker.setup(Predictor.Euler, 1e-5, 1e5, stepping, newton)
        tracker.precision_setup(amp_config_from(s))

        endgame = AMPCauchyEG(tracker)
        obs = mod.GoryDetailLogger()
        endgame.add_observer(obs)

    def test_remove_observer_from_amp_cauchy_endgame(self):
        """Observers should be removable from an AMPCauchyEG."""
        if not self.has_eg_observers:
            self.skipTest("endgame.observers not available")
        mod = getattr(self.eg_obs, 'amp_cauchy', None)
        if mod is None:
            self.skipTest("amp_cauchy observers not available")

        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        from bertini.endgame import AMPCauchyEG
        tracker = AMPTracker(s)
        stepping = SteppingConfig()
        newton = NewtonConfig()
        tracker.setup(Predictor.Euler, 1e-5, 1e5, stepping, newton)
        tracker.precision_setup(amp_config_from(s))

        endgame = AMPCauchyEG(tracker)
        obs = mod.GoryDetailLogger()
        endgame.add_observer(obs)
        endgame.remove_observer(obs)


if __name__ == '__main__':
    unittest.main()
