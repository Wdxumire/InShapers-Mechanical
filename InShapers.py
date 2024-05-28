import numpy as np

    # 输入整形器脉冲生成
    # 生成的脉冲为压缩后的数组，包含时间序列和幅值序列，是一一对应的关系。
# -------------------------------------------------类库---------------------------------------------------------------------

class InShape:
    '整形器类'

    def __init__(self, Freq):
        self.Freq = Freq


class ZVSeries(InShape):
    'ZV整形器类'

    def __init__(self, Freq, zeta):
        super().__init__(Freq)
        self.zeta = zeta


class ZV(ZVSeries):
    'ZV整形器'

    def __init__(self, Freq, zeta):
        super().__init__(Freq, zeta)

    def getCnv(self):
        'ZV Shaper'
        'Freq = Natural Frequency'
        'zeta = Damping Ratio'
        CnvT = np.zeros(2)              
        CnvA = np.zeros(2)
        K = np.exp(-(self.zeta*np.pi/np.sqrt(1-self.zeta**2)))      
        Td = 1/self.Freq/np.sqrt(1-self.zeta**2)                    
        CnvA[0] = 1/(1+K)                                           
        CnvA[1] = 1-CnvA[0]                                         
        CnvT[1] = 0.5*Td                                            
        return CnvT, CnvA, len(CnvT)

# class test(InShape):

#     def __init__(self, Freq):
#         super().__init__(Freq)

#     def getCnv(self):
#         return [0],[1],1

class ZVD(ZVSeries):
    'ZVD整形器'

    def __init__(self, Freq, zeta):
        super().__init__(Freq, zeta)

    def getCnv(self):
        'ZVD Shaper'
        'Freq = Natural Frequency'
        'zeta = Damping Ratio'

        CnvT = np.zeros(3)
        CnvA = np.zeros(3)
        K = np.exp(-(self.zeta*np.pi/np.sqrt(1-self.zeta**2)))
        Td = 1/self.Freq/np.sqrt(1-self.zeta**2)
        CnvA[0] = 1/(1+2*K+K**2)
        CnvA[1] = 2*K/(1+2*K+K**2)
        CnvA[2] = 1-CnvA[1]-CnvA[0]
        CnvT[1] = 0.5*Td
        CnvT[2] = Td
        return CnvT, CnvA, len(CnvT)


class ZVDD(ZVSeries):
    'ZVDD整形器'

    def __init__(self, Freq, zeta):
        super().__init__(Freq, zeta)

    def getCnv(self):
        'ZVDD Shaper'
        'Freq = Natural Frequency'
        'zeta = Damping Ratio'

        CnvT = np.zeros(4)
        CnvA = np.zeros(4)
        K = np.exp(-(self.zeta*np.pi/np.sqrt(1-self.zeta**2)))
        Td = 1/self.Freq/np.sqrt(1-self.zeta**2)
        B = (1+K)**3
        CnvA[0] = 1/B
        CnvA[1] = 3*K/B
        CnvA[2] = 3*K**2/B
        CnvA[3] = 1-CnvA[0]-CnvA[1]-CnvA[2]
        CnvT[1] = 0.5*Td
        CnvT[2] = Td
        CnvT[3] = 1.5*Td
        return CnvT, CnvA, len(CnvT)


class ZVDDD(ZVSeries):
    'ZVDDD整形器'

    def __init__(self, Freq, zeta):
        super().__init__(Freq, zeta)

    def getCnv(self):
        'ZVDDD Shaper'
        'Freq = Natural Frequency'
        'zeta = Damping Ratio'

        CnvT = np.zeros(5)
        CnvA = np.zeros(5)
        K = np.exp(-(self.zeta*np.pi/np.sqrt(1-self.zeta**2)))
        Td = 1/self.Freq/np.sqrt(1-self.zeta**2)
        C = (1+K)**4
        CnvA[0] = 1/C
        CnvA[1] = 4*K/C
        CnvA[2] = 6*K**2/C
        CnvA[3] = 4*K**3/C
        CnvA[4] = 1-CnvA[0]-CnvA[1]-CnvA[2]-CnvA[3]
        CnvT[1] = 0.5*Td
        CnvT[2] = Td
        CnvT[3] = 1.5*Td
        CnvT[4] = 2*Td
        return CnvT, CnvA, len(CnvT)


class MISZV(ZVSeries):
    "ZV整形器修正版"

    def __init__(self, Freq, zeta, n):
        super().__init__(Freq, zeta)
        self.n = n

    def getCnv(self):
        'MISZV-n Shaper'
        'Freq = Natural Frequency'
        'zeta = Damping Ratio'
        'n = number of impulse'

        Td = 1/(self.Freq*np.sqrt(1-self.zeta**2))
        K = np.exp(-2*self.zeta*np.pi/(self.n*np.sqrt(1-self.zeta**2)))
        M = 0
        for i in range(self.n):
            M += K**i

        print(M)

        CnvT = np.zeros(self.n)
        CnvA = np.zeros(self.n)

        for j in range(self.n):
            CnvA[j] = K**j/(1+M)
            CnvT[j] = j*Td/(self.n+1)

        return CnvT, CnvA, len(CnvT)


class EISeries(InShape):
    'EI整形器类'

    def __init__(self, Freq, Tol):
        super().__init__(Freq)
        self.Tol = Tol


class EI(EISeries):
    'EI整形器'

    def __init__(self, Freq, Tol):
        super().__init__(Freq, Tol)

    def getCnv(self):
        'EI Shaper'
        'Freq = Natural Frequency'
        'Tol = Tolerance'

        CnvT = np.zeros(3)
        CnvA = np.zeros(3)
        CnvA[0] = 0.25*(1+self.Tol)
        CnvA[2] = 0.5*(1-self.Tol)
        CnvA[1] = 0.25*(1+self.Tol)
        CnvT[1] = 0.5/self.Freq
        CnvT[2] = 1/self.Freq

        return CnvT, CnvA, len(CnvT)


class H2EI(EISeries):

    '2HEI整形器'

    def __init__(self, Freq, Tol):
        super().__init__(Freq, Tol)

    def getCnv(self):

        '2H-EI Shaper'
        'Freq = Natural Frequency'
        'Tol = Tolerance'

        CnvT = np.zeros(4)
        CnvA = np.zeros(4)
        X = np.cbrt(self.Tol**2*(np.sqrt(1-self.Tol**2)+1))
        CnvA[0] = (3*X**2+2*X+3*self.Tol**2)/16/X
        CnvA[1] = 0.5-CnvA[0]
        CnvA[2] = CnvA[1]
        CnvA[3] = CnvA[0]
        Td = 1/self.Freq
        CnvT[1] = 0.5*Td
        CnvT[2] = Td
        CnvT[3] = 1.5*Td

        return CnvT, CnvA, len(CnvT)


class H3EI(EISeries):
    '3HEI整形器'

    def __init__(self, Freq, Tol):
        super().__init__(Freq, Tol)

    def getCnv(self):
        '2H-EI Shaper'
        'Freq = Natural Frequency'
        'Tol = Tolerance'

        CnvT = np.zeros(5)
        CnvA = np.zeros(5)
        CnvA[0] = (1+3*self.Tol+2*np.sqrt(2*(self.Tol**2+self.Tol)))/16
        CnvA[1] = 0.25*(1-self.Tol)
        CnvA[2] = 1-2*(CnvA[0]+CnvA[1])
        CnvA[3] = CnvA[1]
        CnvA[4] = CnvA[0]
        Td = 1/self.Freq
        CnvT[1] = 0.5*Td
        CnvT[2] = Td
        CnvT[3] = 1.5*Td
        CnvT[4] = 2*Td

        return CnvT, CnvA, len(CnvT)

class compensator:

    def __init__(self,data) -> None:
        self.data = data

    def Compensate(self,T,freq,zeta,alpha):
        omg = 2*3.1415927*freq
        A = T**2*omg**2 + 2*T*omg*zeta + 1
        B = T**2*omg**2+2*T*alpha*omg*zeta + alpha**2
        C = -2*T*omg*zeta - 2
        D = -2*T*alpha*omg*zeta - 2*alpha**2
        E = alpha**2

        yn = []
        yn.append(A*self.data[0]/B)
        yn.append((A*self.data[1]+C*self.data[0]-D*yn[0])/B)
        for i in range(2,len(self.data)):
            y = (A*self.data[i]+C*self.data[i-1]+self.data[i-2]-D*yn[i-1]-E*yn[i-2])/B
            yn.append(y)
        self.yn = yn

