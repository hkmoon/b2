
import numpy as np

rows = 10
cols = 20
rng = np.random.default_rng()


def test(dtype):
    Z = np.zeros((rows, cols), dtype=dtype)
    assert (Z.real == Z.real).all()


# Float
test(np.csingle)
# Double
test(np.cdouble)
# Long Double
test(np.clongdouble)
