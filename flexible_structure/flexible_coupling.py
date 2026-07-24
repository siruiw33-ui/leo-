import numpy as np


class FlexibleCoupling:

    def __init__(self,
                 J):

        self.J = J

        Mf = self.Mf
        Cf = self.Cf
        Kf = self.Kf

        def build_state_matrix(self):

            n = self.Mr.shape[0]

            A = np.zeros((6+2*n, 6+2*n))

            A[0:3, 3:6] = np.eye(3)

            A[6+n:,6:6+n] = -np.linalg.inv(self.Mr)@self.Kr

            A[6 + n:,6 + n:] = -np.linalg.inv(self.Mr) @ self.Cr

            return A


