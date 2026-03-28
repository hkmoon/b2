# This file is part of Bertini 2.
#
# python/test/tracking/config_test.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python/test/tracking/config_test.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python/test/tracking/config_test.py.  If not, see <http://www.gnu.org/licenses/>.
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

try:
    from bertini import *
    from bertini.function_tree.symbol import *
    from bertini.function_tree.root import *
    from bertini.function_tree import *
    from bertini.tracking import *
    from bertini.tracking.config import *
    from bertini.endgame.config import *
    import bertini.multiprec as mp
    from bertini.multiprec import Float as mpfr_float
    from bertini.multiprec import Complex as mpfr_complex
    HAS_BERTINI = True
except ImportError:
    HAS_BERTINI = False


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class SteppingConfigTest(unittest.TestCase):
    """Tests for the SteppingConfig tracking configuration."""

    def test_instantiation(self):
        """SteppingConfig should be instantiable with no arguments."""
        cfg = SteppingConfig()
        self.assertIsNotNone(cfg)

    def test_initial_step_size_readable(self):
        """initial_step_size should be readable and have a positive default."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.initial_step_size, 0)

    def test_max_step_size_readable(self):
        """max_step_size should be readable and have a positive default."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.max_step_size, 0)

    def test_min_step_size_readable(self):
        """min_step_size should be readable and have a positive default."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.min_step_size, 0)

    def test_step_size_success_factor_readable(self):
        """step_size_success_factor should be readable and positive."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.step_size_success_factor, 0)

    def test_step_size_fail_factor_readable(self):
        """step_size_fail_factor should be readable and positive."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.step_size_fail_factor, 0)

    def test_consecutive_successful_steps_readable(self):
        """consecutive_successful_steps_before_stepsize_increase should be a positive integer."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.consecutive_successful_steps_before_stepsize_increase, 0)

    def test_min_num_steps_readable(self):
        """min_num_steps should be readable."""
        cfg = SteppingConfig()
        self.assertIsNotNone(cfg.min_num_steps)

    def test_max_num_steps_readable(self):
        """max_num_steps should be readable and positive."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.max_num_steps, 0)

    def test_frequency_of_CN_estimation_readable(self):
        """frequency_of_CN_estimation should be readable and positive."""
        cfg = SteppingConfig()
        self.assertGreater(cfg.frequency_of_CN_estimation, 0)

    def test_modify_initial_step_size(self):
        """initial_step_size should be modifiable."""
        cfg = SteppingConfig()
        cfg.initial_step_size = 0.05
        self.assertAlmostEqual(cfg.initial_step_size, 0.05)

    def test_modify_max_step_size(self):
        """max_step_size should be modifiable."""
        cfg = SteppingConfig()
        cfg.max_step_size = 0.5
        self.assertAlmostEqual(cfg.max_step_size, 0.5)

    def test_modify_min_step_size(self):
        """min_step_size should be modifiable."""
        cfg = SteppingConfig()
        cfg.min_step_size = 1e-20
        self.assertAlmostEqual(cfg.min_step_size, 1e-20)

    def test_modify_max_num_steps(self):
        """max_num_steps should be modifiable."""
        cfg = SteppingConfig()
        cfg.max_num_steps = 50000
        self.assertEqual(cfg.max_num_steps, 50000)

    def test_modify_consecutive_successful_steps(self):
        """consecutive_successful_steps_before_stepsize_increase should be modifiable."""
        cfg = SteppingConfig()
        cfg.consecutive_successful_steps_before_stepsize_increase = 10
        self.assertEqual(cfg.consecutive_successful_steps_before_stepsize_increase, 10)

    def test_step_size_ordering(self):
        """min_step_size should be less than or equal to max_step_size by default."""
        cfg = SteppingConfig()
        self.assertLessEqual(cfg.min_step_size, cfg.max_step_size)

    def test_used_in_tracker_setup(self):
        """SteppingConfig should be usable in tracker.setup()."""
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
        stepping = SteppingConfig()
        stepping.max_num_steps = 20000
        newton = NewtonConfig()
        tracker.setup(Predictor.Euler, 1e-5, 1e5, stepping, newton)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class NewtonConfigTest(unittest.TestCase):
    """Tests for the NewtonConfig tracking configuration."""

    def test_instantiation(self):
        """NewtonConfig should be instantiable with no arguments."""
        cfg = NewtonConfig()
        self.assertIsNotNone(cfg)

    def test_max_num_newton_iterations_readable(self):
        """max_num_newton_iterations should be readable and positive."""
        cfg = NewtonConfig()
        self.assertGreater(cfg.max_num_newton_iterations, 0)

    def test_min_num_newton_iterations_readable(self):
        """min_num_newton_iterations should be readable."""
        cfg = NewtonConfig()
        self.assertIsNotNone(cfg.min_num_newton_iterations)

    def test_modify_max_num_newton_iterations(self):
        """max_num_newton_iterations should be modifiable."""
        cfg = NewtonConfig()
        cfg.max_num_newton_iterations = 5
        self.assertEqual(cfg.max_num_newton_iterations, 5)

    def test_modify_min_num_newton_iterations(self):
        """min_num_newton_iterations should be modifiable."""
        cfg = NewtonConfig()
        cfg.min_num_newton_iterations = 2
        self.assertEqual(cfg.min_num_newton_iterations, 2)

    def test_used_in_tracker_setup(self):
        """NewtonConfig should be usable in tracker.setup()."""
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
        stepping = SteppingConfig()
        newton = NewtonConfig()
        newton.max_num_newton_iterations = 3
        tracker.setup(Predictor.Euler, 1e-5, 1e5, stepping, newton)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class AMPConfigTest(unittest.TestCase):
    """Tests for the AMPConfig (AdaptiveMultiplePrecisionConfig)."""

    def test_instantiation_default(self):
        """AMPConfig should be instantiable with no arguments."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg)

    def test_instantiation_from_system(self):
        """AMPConfig should be instantiable from a System."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        cfg = AMPConfig(s)
        self.assertIsNotNone(cfg)

    def test_amp_config_from_function(self):
        """amp_config_from() should create an AMPConfig from a System."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        cfg = amp_config_from(s)
        self.assertIsNotNone(cfg)

    def test_safety_digits_readable(self):
        """safety_digits_1 and safety_digits_2 should be readable."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg.safety_digits_1)
        self.assertIsNotNone(cfg.safety_digits_2)

    def test_maximum_precision_readable(self):
        """maximum_precision should be readable and positive."""
        cfg = AMPConfig()
        self.assertGreater(cfg.maximum_precision, 0)

    def test_modify_safety_digits(self):
        """safety_digits should be modifiable."""
        cfg = AMPConfig()
        cfg.safety_digits_1 = 2
        self.assertEqual(cfg.safety_digits_1, 2)
        cfg.safety_digits_2 = 3
        self.assertEqual(cfg.safety_digits_2, 3)

    def test_modify_maximum_precision(self):
        """maximum_precision should be modifiable."""
        cfg = AMPConfig()
        cfg.maximum_precision = 512
        self.assertEqual(cfg.maximum_precision, 512)

    def test_epsilon_readable(self):
        """epsilon should be readable."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg.epsilon)

    def test_phi_psi_readable(self):
        """phi and psi should be readable."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg.phi)
        self.assertIsNotNone(cfg.psi)

    def test_coefficient_bound_readable(self):
        """coefficient_bound should be readable."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg.coefficient_bound)

    def test_degree_bound_readable(self):
        """degree_bound should be readable."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg.degree_bound)

    def test_set_amp_config_from_system(self):
        """set_amp_config_from should populate config from a System."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x**2 - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        cfg = AMPConfig()
        cfg.set_amp_config_from(s)

    def test_consecutive_successful_steps_before_precision_decrease(self):
        """consecutive_successful_steps_before_precision_decrease should be readable and modifiable."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg.consecutive_successful_steps_before_precision_decrease)
        cfg.consecutive_successful_steps_before_precision_decrease = 10
        self.assertEqual(cfg.consecutive_successful_steps_before_precision_decrease, 10)

    def test_max_num_precision_decreases(self):
        """max_num_precision_decreases should be readable and modifiable."""
        cfg = AMPConfig()
        self.assertIsNotNone(cfg.max_num_precision_decreases)
        cfg.max_num_precision_decreases = 5
        self.assertEqual(cfg.max_num_precision_decreases, 5)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class FixedPrecisionConfigTest(unittest.TestCase):
    """Tests for the FixedPrecisionConfig."""

    def test_instantiation_from_system(self):
        """FixedPrecisionConfig should be instantiable from a System."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        cfg = FixedPrecisionConfig(s)
        self.assertIsNotNone(cfg)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class EndgameConfigTest(unittest.TestCase):
    """Tests for endgame configuration classes."""

    def test_endgame_config_instantiation(self):
        """Endgame config should be instantiable with no arguments."""
        cfg = Endgame()
        self.assertIsNotNone(cfg)

    def test_endgame_num_sample_points_readable(self):
        """num_sample_points should be readable and positive."""
        cfg = Endgame()
        self.assertGreater(cfg.num_sample_points, 0)

    def test_endgame_min_track_time_readable(self):
        """min_track_time should be readable."""
        cfg = Endgame()
        self.assertIsNotNone(cfg.min_track_time)

    def test_endgame_sample_factor_readable(self):
        """sample_factor should be readable and positive."""
        cfg = Endgame()
        self.assertGreater(cfg.sample_factor, 0)

    def test_endgame_final_tolerance_readable(self):
        """final_tolerance should be readable and positive."""
        cfg = Endgame()
        self.assertGreater(cfg.final_tolerance, 0)

    def test_endgame_max_num_newton_iterations_readable(self):
        """max_num_newton_iterations should be readable and positive."""
        cfg = Endgame()
        self.assertGreater(cfg.max_num_newton_iterations, 0)

    def test_modify_endgame_num_sample_points(self):
        """num_sample_points should be modifiable."""
        cfg = Endgame()
        cfg.num_sample_points = 5
        self.assertEqual(cfg.num_sample_points, 5)

    def test_modify_endgame_final_tolerance(self):
        """final_tolerance should be modifiable."""
        cfg = Endgame()
        cfg.final_tolerance = 1e-12
        self.assertAlmostEqual(cfg.final_tolerance, 1e-12)

    def test_modify_endgame_sample_factor(self):
        """sample_factor should be modifiable."""
        cfg = Endgame()
        cfg.sample_factor = 0.6
        self.assertAlmostEqual(cfg.sample_factor, 0.6)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class SecurityConfigTest(unittest.TestCase):
    """Tests for the Security endgame configuration."""

    def test_instantiation(self):
        """Security config should be instantiable with no arguments."""
        cfg = Security()
        self.assertIsNotNone(cfg)

    def test_level_readable(self):
        """level should be readable."""
        cfg = Security()
        self.assertIsNotNone(cfg.level)

    def test_max_norm_readable(self):
        """max_norm should be readable and positive."""
        cfg = Security()
        self.assertGreater(cfg.max_norm, 0)

    def test_modify_level(self):
        """level should be modifiable."""
        cfg = Security()
        cfg.level = 1
        self.assertEqual(cfg.level, 1)
        cfg.level = 0
        self.assertEqual(cfg.level, 0)

    def test_modify_max_norm(self):
        """max_norm should be modifiable."""
        cfg = Security()
        cfg.max_norm = 1e8
        self.assertAlmostEqual(cfg.max_norm, 1e8)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class PowerSeriesConfigTest(unittest.TestCase):
    """Tests for the PowerSeriesConfig endgame configuration."""

    def test_instantiation(self):
        """PowerSeriesConfig should be instantiable with no arguments."""
        cfg = PowerSeriesConfig()
        self.assertIsNotNone(cfg)

    def test_max_cycle_number_readable(self):
        """max_cycle_number should be readable and positive."""
        cfg = PowerSeriesConfig()
        self.assertGreater(cfg.max_cycle_number, 0)

    def test_cycle_number_amplification_readable(self):
        """cycle_number_amplification should be readable and positive."""
        cfg = PowerSeriesConfig()
        self.assertGreater(cfg.cycle_number_amplification, 0)

    def test_modify_max_cycle_number(self):
        """max_cycle_number should be modifiable."""
        cfg = PowerSeriesConfig()
        cfg.max_cycle_number = 10
        self.assertEqual(cfg.max_cycle_number, 10)

    def test_modify_cycle_number_amplification(self):
        """cycle_number_amplification should be modifiable."""
        cfg = PowerSeriesConfig()
        cfg.cycle_number_amplification = 100
        self.assertEqual(cfg.cycle_number_amplification, 100)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class CauchyConfigTest(unittest.TestCase):
    """Tests for the CauchyConfig endgame configuration."""

    def test_instantiation(self):
        """CauchyConfig should be instantiable with no arguments."""
        cfg = CauchyConfig()
        self.assertIsNotNone(cfg)

    def test_cycle_cutoff_time_readable(self):
        """cycle_cutoff_time should be readable."""
        cfg = CauchyConfig()
        self.assertIsNotNone(cfg.cycle_cutoff_time)

    def test_ratio_cutoff_time_readable(self):
        """ratio_cutoff_time should be readable."""
        cfg = CauchyConfig()
        self.assertIsNotNone(cfg.ratio_cutoff_time)

    def test_maximum_cauchy_ratio_readable(self):
        """maximum_cauchy_ratio should be readable and positive."""
        cfg = CauchyConfig()
        self.assertGreater(cfg.maximum_cauchy_ratio, 0)

    def test_num_needed_for_stabilization_readable(self):
        """num_needed_for_stabilization should be readable and positive."""
        cfg = CauchyConfig()
        self.assertGreater(cfg.num_needed_for_stabilization, 0)

    def test_fail_safe_maximum_cycle_number_readable(self):
        """fail_safe_maximum_cycle_number should be readable and positive."""
        cfg = CauchyConfig()
        self.assertGreater(cfg.fail_safe_maximum_cycle_number, 0)

    def test_modify_maximum_cauchy_ratio(self):
        """maximum_cauchy_ratio should be modifiable."""
        cfg = CauchyConfig()
        cfg.maximum_cauchy_ratio = 0.8
        self.assertAlmostEqual(cfg.maximum_cauchy_ratio, 0.8)

    def test_modify_num_needed_for_stabilization(self):
        """num_needed_for_stabilization should be modifiable."""
        cfg = CauchyConfig()
        cfg.num_needed_for_stabilization = 5
        self.assertEqual(cfg.num_needed_for_stabilization, 5)

    def test_modify_fail_safe_maximum_cycle_number(self):
        """fail_safe_maximum_cycle_number should be modifiable."""
        cfg = CauchyConfig()
        cfg.fail_safe_maximum_cycle_number = 25
        self.assertEqual(cfg.fail_safe_maximum_cycle_number, 25)


@unittest.skipUnless(HAS_BERTINI, "pybertini not available")
class EndgameConfigIntegrationTest(unittest.TestCase):
    """Integration tests: configs used with actual endgame objects."""

    def test_endgame_config_with_amp_cauchy(self):
        """Endgame config should be settable on an AMPCauchyEG instance."""
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

        eg = AMPCauchyEG(tracker)

        eg_cfg = Endgame()
        eg_cfg.num_sample_points = 4
        eg_cfg.final_tolerance = 1e-12
        eg.set_endgame_settings(eg_cfg)

        retrieved_cfg = eg.get_endgame_settings()
        self.assertEqual(retrieved_cfg.num_sample_points, 4)

    def test_security_config_with_amp_cauchy(self):
        """Security config should be settable on an AMPCauchyEG instance."""
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

        eg = AMPCauchyEG(tracker)

        sec_cfg = Security()
        sec_cfg.level = 1
        sec_cfg.max_norm = 1e6
        eg.set_security_settings(sec_cfg)

        retrieved_cfg = eg.get_security_settings()
        self.assertEqual(retrieved_cfg.level, 1)

    def test_cauchy_config_with_amp_cauchy_constructor(self):
        """CauchyConfig should be passable to AMPCauchyEG constructor."""
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

        cauchy_cfg = CauchyConfig()
        eg = AMPCauchyEG(tracker, cauchy_cfg)
        self.assertIsNotNone(eg)

    def test_pseg_config_with_amp_pseg_constructor(self):
        """PowerSeriesConfig should be passable to AMPPSEG constructor."""
        default_precision(30)
        x = Variable("x")
        t = Variable("t")
        s = System()
        vg = VariableGroup()
        vg.append(x)
        s.add_function(x - t)
        s.add_path_variable(t)
        s.add_variable_group(vg)

        from bertini.endgame import AMPPSEG
        tracker = AMPTracker(s)
        stepping = SteppingConfig()
        newton = NewtonConfig()
        tracker.setup(Predictor.Euler, 1e-5, 1e5, stepping, newton)
        tracker.precision_setup(amp_config_from(s))

        ps_cfg = PowerSeriesConfig()
        eg = AMPPSEG(tracker, ps_cfg)
        self.assertIsNotNone(eg)

    def test_tracker_get_set_stepping_config(self):
        """Tracker should support get_stepping and set_stepping."""
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
        stepping = SteppingConfig()
        newton = NewtonConfig()
        tracker.setup(Predictor.Euler, 1e-5, 1e5, stepping, newton)

        retrieved = tracker.get_stepping()
        self.assertIsNotNone(retrieved)

        new_stepping = SteppingConfig()
        new_stepping.max_num_steps = 30000
        tracker.set_stepping(new_stepping)

        updated = tracker.get_stepping()
        self.assertEqual(updated.max_num_steps, 30000)

    def test_tracker_get_set_newton_config(self):
        """Tracker should support get_newton and set_newton."""
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
        stepping = SteppingConfig()
        newton = NewtonConfig()
        tracker.setup(Predictor.Euler, 1e-5, 1e5, stepping, newton)

        retrieved = tracker.get_newton()
        self.assertIsNotNone(retrieved)

        new_newton = NewtonConfig()
        new_newton.max_num_newton_iterations = 7
        tracker.set_newton(new_newton)

        updated = tracker.get_newton()
        self.assertEqual(updated.max_num_newton_iterations, 7)


if __name__ == '__main__':
    unittest.main()
