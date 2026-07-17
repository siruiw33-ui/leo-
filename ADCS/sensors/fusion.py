import numpy as np

class SensorFusion:

    def __init__(
        self,
        gyro=None,
        star_tracker=None,
        gps=None,
        sun_sensor=None,
        magnetometer=None):

        #传感器
        self.gyro = gyro
        self.star_tracker = star_tracker
        self.gps = gps
        self.sun_sensor = sun_sensor
        self.magnetometer = magnetometer


    #更新测量
    def measure(self,state):

        measurement={}

        #陀螺仪测量角速度
        if self.gyro is not None:
            measurement["gyro"] = (self.gyro.measure(state["omega"]))

        # 星敏感器测量姿态
        if self.star_tracker is not None:
            measurement["star_tracker"] = (self.star_tracker.measure(state["q"]))

        # GPS测量速度和位置
        if self.gps is not None:
            measurement["gps"] = (self.gps.measure(state["r"],state["v"]))

        # 太阳敏感器测量
        if self.sun_sensor is not None:
            measurement["sun_sensor"] = (self.sun_sensor.measure(state["sun_body"]))

        # 磁强计测量磁场强度
        if self.magnetometer is not None:
            measurement["magnetometer"]=(self.magnetometer.measure(state["B_body"]))

        return measurement