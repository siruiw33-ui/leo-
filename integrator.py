from scipy.integrate import solve_ivp
from orbit.concatenate import dynamics


def propagate(state0, t0, tf):

    solution = solve_ivp(
        dynamics,
        (t0, tf),
        state0,
        method="RK45",
        rtol=1e-9,
        atol=1e-9
    )

    return solution