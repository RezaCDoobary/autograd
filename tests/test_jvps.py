import autograd.numpy as np
from autograd.core import vspace, make_jvp, flatten

EPS, RTOL, ATOL = 1e-4, 1e-4, 1e-6

def linear_fun_to_matrix(flat_fun, vs):
    return np.stack(map(flat_fun, np.eye(vs.size)))

def flatten_fun(fun, vs):
    return lambda x : flatten(fun(vs.unflatten(x)))

def numerical_deriv(flat_fun, arg):
    return lambda x : (  flat_fun(arg + EPS/2 * x)
                       - flat_fun(arg - EPS/2 * x) ) / EPS

def check_jvp(fun, arg):
    vs_in  = vspace(arg)
    vs_out = vspace(fun(arg))
    autograd_jac  = linear_fun_to_matrix(
        flatten_fun(make_jvp(fun)(arg)[0], vs_out), vs_out).T
    numerical_jac = linear_fun_to_matrix(
        numerical_deriv(flatten_fun(fun, vs_in), flatten(arg)), vs_in)

    assert np.allclose(autograd_jac, numerical_jac)

def test_sin():
    check_jvp(np.sin, 1.0)
