"""

"""

import numpy as np

from attitude.quaternion import to_dcm
from orbit.geomagnetic import magnetic_field
from constants import Km


def magnetic_torque(
    t,
    q,
    r,
    current_cmd,
    current_noise_model,
    residual_model,
    dt,):

    B_eci = magnetic_field(t)

    C = to_dcm(q)
    B_body = (C.T @ B_eci)

    # 电流噪声模型
    current_actual = (current_noise_model.step(current_cmd=current_cmd,dt=dt))

    # 剩磁模型
    residual_magnetic = (residual_model.update(current=current_actual,dt=dt))

    #  控制磁偶极矩
    magnetic_dipole = (Km @ current_actual)

    # 总磁偶极矩
    m = ( residual_magnetic+ magnetic_dipole)

    # 磁力矩
    torque = np.cross(m,B_body)

    return torque