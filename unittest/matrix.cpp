#include <boost/python.hpp>

#include "bertini2/eigen_extensions.hpp"

#include <Eigen/Dense>
#include <Eigen/LU>

using mpfr_float = bertini::mpfr_float;

// this test assures that the Eigen::NumTraits defined in eigen_extensions.hpp is correctly found during template instantiation, and that the Real type it defines is actually mpfr_float.  If it were not, then we would be unable to make an expression of ::Real type in variable q, because it would be an expression, not a populatable number of type mpfr_float.
BOOST_AUTO_TEST_CASE(matrix) {
	using NumT = bertini::mpfr_float;

	NumT a {1}, b{2}, c{3};

	Eigen::NumTraits<decltype(a*a + b*b/ c)>::Real q{0};
}
