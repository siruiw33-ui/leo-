"""
组合太阳翼、支撑梁、光学平台
"""

import numpy as np

from solar_wing.solar_model import SolarWing
from support_beam.support_model import SupportBeam
from optical_platform.platform_model import OpticalPlatform


class FlexibleSystem:


    def __init__(
        self,
        solar = SolarWing(),
        support = SupportBeam(),
        platform = OpticalPlatform(),):

        self.solar = solar
        self.support = support
        self.platform = platform

    def build(self):

        Ms,Cs,Ks = self.solar.build()

        Mb,Cb,Kb = self.support.build()

        Mp,Cp,Kp = self.platform.build()

        self.Mf = self.block_matrix(Ms,Mb,Mp)

        self.Cf = self.block_matrix(Cs,Cb,Cp)

        self.Kf = self.block_matrix(Ks,Kb,Kp)


        return (self.Mf, self.Cf, self.Kf)


    def block_matrix( self, A,B,C):

        n1=A.shape[0]
        n2=B.shape[0]
        n3=C.shape[0]

        M=np.zeros((n1+n2+n3, n1+n2+n3))

        M[0:n1, 0:n1]=A

        M[n1:n1+n2, n1:n1+n2]=B

        M[n1+n2:, n1+n2: ]=C

        return M