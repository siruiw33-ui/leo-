"""
磁力矩器电流噪声
"""

import numpy as np
import matplotlib.pyplot as plt
from disturbance.current_noise import MagnetorquerCurrentNoise

#步长
dt = 0.001
#总仿真时间
T = 10.0
#时间数组
time = np.arange(0.0, T, dt)
#仿真步长
N = len(time)


current_model = MagnetorquerCurrentNoise(
    tau=0.01,
    lambda_bias=0.001,
    sigma_current=1e-4,
    sigma_bias=1e-6,
    current_limit=0.5,)


#定义阶跃输入
def current_command(t):
    if t < 1.0:
        return np.array([0.0, 0.0, 0.0])
    elif t < 4.0:
        return np.array([0.1, 0.0, 0.0])
    elif t < 7.0:
        return np.array([0.2, 0.0, 0.0])
    else:
        return np.array([0.0, 0.0, 0.0])

#存储电流历史
current_cmd_history = np.zeros((N, 3))
#存储实际输出电流历史
current_actual_history = np.zeros((N, 3))
#存储偏置漂移
bias_history = np.zeros((N, 3))

for k, t in enumerate(time):

    current_cmd = current_command(t)
    current_actual = current_model.step(current_cmd=current_cmd,dt=dt)

    current_cmd_history[k] = current_cmd
    current_actual_history[k] = current_actual
    bias_history[k] = current_model.bias.copy()

#电流误差
current_error = (current_actual_history- current_cmd_history)

#提取8秒后的稳态数据
steady_state_index = time >= 8.0
steady_error = current_error[steady_state_index, 0]

#计算稳态误差的统计特征
mean_error = np.mean(steady_error)          #均值
std_error = np.std(steady_error)            #标准差
max_error = np.max(np.abs(steady_error))    #最大绝对误差

#限幅电流判断
max_current = np.max(np.abs(current_actual_history))
if max_current <= current_model.current_limit:
    print("Saturation test: PASS")
else:
    print("Saturation test: FAIL")


#图1 电流动态响应
plt.figure(figsize=(10, 5))
plt.plot( time,current_cmd_history[:, 0],label="Command current")
plt.plot(time,current_actual_history[:, 0],label="Actual current")

plt.xlabel("Time [s]")
plt.ylabel("Current [A]")
plt.title("Magnetorquer Current Dynamic Response")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#图2 电流误差时间历程
plt.figure(figsize=(10, 5))
plt.plot(time,current_error[:, 0],label="Current error X")
plt.axhline(0.0,linestyle="--")

plt.xlabel("Time [s]")
plt.ylabel("Current error [A]")
plt.title("Magnetorquer Current Error")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#图3 电流偏置变化图
plt.figure(figsize=(10, 5))
plt.plot(time,bias_history[:, 0],label="Bias X")
plt.plot(time,bias_history[:, 1],label="Bias Y")
plt.plot(time,bias_history[:, 2],label="Bias Z")
plt.axhline(0.0,linestyle="--")

plt.xlabel("Time [s]")
plt.ylabel("Current bias [A]")
plt.title("Magnetorquer Current Bias Evolution")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#图4 稳态电流误差的直方图
plt.figure(figsize=(8, 5))
plt.hist(steady_error,bins=50)
plt.xlabel("Current error [A]")
plt.ylabel("Frequency")
plt.title("Steady-State Current Error Distribution")
plt.grid(True)
plt.tight_layout()
plt.show()


saturation_model = MagnetorquerCurrentNoise(
    tau=0.01,
    lambda_bias=0.001,
    sigma_current=0.0,
    sigma_bias=0.0,
    current_limit=0.5,)

saturation_time = np.arange(0.0, 1.0, dt)
saturation_current = np.zeros(len(saturation_time))

for k, t in enumerate(saturation_time):

    current_actual = saturation_model.step(current_cmd=np.array([1.0, 0.0, 0.0]),dt=dt)
    saturation_current[k] = current_actual[0]



#图5 饱和验证图
plt.figure(figsize=(10, 5))
plt.plot(saturation_time,saturation_current,label="Actual current")
plt.axhline(0.5,linestyle="--",label="Upper limit")
plt.axhline(-0.5,linestyle="--",label="Lower limit")

plt.xlabel("Time [s]")
plt.ylabel("Current [A]")
plt.title("Magnetorquer Current Saturation Verification")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()