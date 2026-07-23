"""
四节点矩形单元建模
"""
import numpy as np

class PlateElement:

    def __init__(
        self,
        E,
        h,
        nu,
        rho,
        a,
        b):

        self.E=E

        self.h=h
        #泊松比
        self.nu=nu

        self.rho=rho

        #x方向边长
        self.a=a
        #y方向边长
        self.b=b

    def bending_matrix(self):

        D = ( self.E*self.h**3/ (12*(1-self.nu**2)))
        Db=D*np.array([
                [1,self.nu,0],

                [self.nu,1,0],

                [0,0,(1-self.nu)/2]])

        return Db


    def stiffness_matrix(self):

        D = self.bending_matrix()

        Ke = np.zeros((12, 12))

        #高斯积分坐标
        gauss_points=[
            (-1/np.sqrt(3), -1/np.sqrt(3)),

            (1/np.sqrt(3), -1/np.sqrt(3)),

            (1/np.sqrt(3), 1/np.sqrt(3)),

            (-1/np.sqrt(3), 1/np.sqrt(3)) ]

        weight=1

        for xi,eta in gauss_points:

            B = self.B_matrix(xi, eta)

            detJ = self.a*self.b/4

            Ke += (B.T@D@B * detJ * weight )

        return Ke


    def mass_matrix(self):

        Me = np.zeros((12,12))

        area = self.a * self.b

        mass = (self.rho * self.h * area / 4 )

        for i in range(4):

            index=3*i

            Me[index,index]=mass

        return Me


    def B_matrix(self, xi,eta ):

        B=np.zeros( (3,12))

        return B