import numpy as np
from integrator import propagate
from visualization import plot_orbit



#初始状态的数据输入
r0 = np.array([6928e3,0,0])
v0 = np.array([0,7585,0])
state0 = np.concatenate((r0, v0))

solution = propagate(
    state0,
    0,
    5400
)

plot_orbit(solution)
