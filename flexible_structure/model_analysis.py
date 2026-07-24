"""
模态分析
"""

import numpy as np
from scipy.linalg import eigh
class ModalAnalysis:

    def __init__( self, M, K):
        self.M=M
        self.K=K


    def solve( self, modes=10):

        eigenvalues,eigenvectors=eigh(self.K, self.M)

        omega=np.sqrt(eigenvalues)

        frequency=omega/(2*np.pi)

        omega=omega[:modes]

        frequency=frequency[:modes]

        Phi=eigenvectors[:,:modes]

        return (frequency,Phi)