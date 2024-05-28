import numpy as np
import InShapers as IS
class Profile:
    '点对点运动规划'
    __ISOn = False                                  #输入整形功能的flag
    __ISCompOn = False                              #自动补偿功能的flag
    __Tj1 = 0                                         #Jerk加速段时间
    __Tj2 = 0                                         #Jerk减速段时间
    __Ta = 0                                          #加速段时间
    __Td = 0                                          #减速段时间
    __Tv = 0                                          #匀速段时间
    alpha = 1
    
    def __init__(self,vel,acc,dec,jerk):
        '设定速度、加速度、减速度、Jerk'
        self.vel = vel
        self.acc = acc
        self.dec = dec
        self.jerk = jerk
        self.intval = 0.1
        self.length = 100
    
    def intval_conf(self,intval):
        '设定插补周期'
        self.intval = intval

    def length_conf(self,length):
        '设定信号长度'
        self.length = length

    def ISCompensateON(self,T,freq,zeta):
        self.__ISCompOn = True
        '开启自动补偿（低代价）'
        self.T = T
        self.freq = freq
        self.zeta = zeta
        print("开启自动补偿（低代价）")
        pass

    def ISCompensateOff(self):
        self.__ISCompOn = False
        self.alpha = 1
        print("关闭自动补偿（低代价）")


    def InShapeOn(self,obj):
        self.__ISOn = True
        self.CnvT = obj.getCnv()[0]
        self.CnvA = obj.getCnv()[1]
        print("整形器已开启（幅值序列，时间序列）",self.CnvA,self.CnvT)
    
    def InShapeOff(self):
        self.__ISOn = False
        print("整形器已关闭")

    def __profileSpdGen(self):
        # 速度规划参数预生成
        if self.vel > self.acc**2/self.jerk:
            #存在匀加速段
            self.__Tj1 = self.acc/self.jerk
            self.__Ta = self.vel/self.acc-self.__Tj1
        else:
            #不存在匀加速段
            self.acc = np.sqrt(self.vel*self.jerk)
            self.__Tj1 = self.acc/self.jerk
            self.__Ta = 0
        if self.vel > self.dec**2/self.jerk:
            #存在匀减速段
            self.__Tj2 = self.dec/self.jerk
            self.__Td = self.vel/self.dec-self.__Tj2
        else:
            #不存在匀减速段
            self.dec = np.sqrt(self.vel*self.jerk)
            self.__Tj2 = self.dec/self.jerk
            self.__Td = 0
    
    def __dispCalc(self):
        dispA = 0.5*self.jerk*self.__Tj1**2*(self.__Ta+self.__Tj1)+0.5*self.jerk*self.__Tj1*(self.__Ta+self.__Tj1)**2
        dispB = 0.5*self.jerk*self.__Tj2**2*(self.__Td+self.__Tj2)+0.5*self.jerk*self.__Tj2*(self.__Td+self.__Tj2)**2
        return dispA+dispB


    def __binRAMethod(self,disp,v_start,v_end):
        # 使用递归方法实现二分法迭代
        # 递归出口，避免死循环

        if v_start>v_end:
            return 0
        
        # 使临时最大速度处于索引中间位置
        self.vel= v_start+(v_end-v_start)/2
        self.__profileSpdGen()
        self.__dispCalc()
        if abs(disp-self.__dispCalc()) <= 0.0001:
            self.__Tv = 0
            # print(self.__Tj1,self.__Ta,self.__Tj1,self.__Tv,self.__Tj2,self.__Td,self.__Tj2)
        elif disp-self.__dispCalc() > 0.0001:
            self.__binRAMethod(disp,self.vel,v_end)
        else:
            self.__binRAMethod(disp,v_start,self.vel)
            
        
    def scopeGen(self):
        Time = []
        Jerk = []
        Acc = []
        Vel = []
        t1 = self.__Tj1
        t2 = self.__Ta+self.__Tj1
        t3 = self.__Ta+2*self.__Tj1
        t4 = self.__Ta+2*self.__Tj1+self.__Tv
        t5 = self.__Ta+2*self.__Tj1+self.__Tv+self.__Tj2
        t6 = self.__Ta+2*self.__Tj1+self.__Tv+self.__Tj2+self.__Td
        t7 = self.__Ta+2*self.__Tj1+self.__Tv+2*self.__Tj2+self.__Td
        C1 = 0.5*self.jerk*t1**2
        C2 = C1 + self.acc*self.__Ta + 0.5*self.jerk*self.__Tj1**2
        C3 = -0.5*self.jerk*self.__Tj2**2+self.vel
        C4 = C3 - self.dec*self.__Td-0.5*self.jerk*self.__Tj2**2


        # disp_now = 0

        for i in range(int(self.length/1000/self.intval)):
            t = i*self.intval
            Time.append(t)

            if t <= t1:
                Jerk.append(self.jerk)
                Acc.append(self.jerk*t)
                Vel.append(0.5*self.jerk*t**2)

            elif t <= t2 and t > t1:
                Jerk.append(0)
                Acc.append(self.jerk*t1)
                Vel.append(C1+self.acc*(t-t1))

            elif t <= t3 and t > t2:
                Jerk.append(-self.jerk)
                Acc.append(self.jerk*(t3-t))
                Vel.append(C2-0.5*self.jerk*(t3-t)**2)

            elif t <= t4 and t > t3:
                Jerk.append(0)
                Acc.append(0)
                Vel.append(self.vel)

            elif t <= t5 and t > t4:
                Jerk.append(-self.jerk)
                Acc.append(self.jerk*(t4-t))
                Vel.append(self.vel - 0.5*self.jerk*(t4-t)**2)

            elif t <= t6 and t > t5:
                Jerk.append(0)
                Acc.append(-self.dec)
                Vel.append(C3 - self.dec*(t-t5))

            elif t <= t7 and t > t6:
                Jerk.append(self.jerk)
                Acc.append(self.jerk*(t-t7))
                Vel.append(C4+0.5*self.jerk*(t-t7)**2)

            else:
                Jerk.append(0)
                Acc.append(0)
                Vel.append(0)
            

            

        return Time, Jerk, Acc, Vel, t7#, Disp


    
    def ptp(self, disp):
        '点对点运动'
        #规划速度曲线参数
        #各个时间段求解，self.__Tj1，self.__Tj2为加速段，减速段Jerk时间，self.__Ta为加速段时间，self.__Td为减速段时间，self.__Tv为匀速段时间。
        #先进行速度规划
        self.__profileSpdGen()
        #判断是否存在匀速段
        if disp >= self.__dispCalc():
            # 有匀速段的情况下，直接算出匀速段的持续时间
            self.__Tv = (disp-self.__dispCalc())/self.vel
            # print(self.__Tj1,self.__Ta,self.__Tj1,self.__Tv,self.__Tj2,self.__Td,self.__Tj2)
        else:
            # 没有匀速段的情况下，通过二分法对最大速度进行修改，并重新规划
            self.__binRAMethod(disp,0,self.vel)
        
        res = self.scopeGen()
        #获取总时间大小
        self.total_time = res[4]
        #获取时间轴
        self.time_line = res[0]
        #获取加速度
        self.acc_line = res[2]
        #获取速度
        self.vel_line = res[3]
        #获取jerk
        self.jerk_line = res[1]
        # 如果开启了自动补偿
        if self.__ISCompOn:
            self.alpha = self.total_time/(self.total_time+self.CnvT[len(self.CnvT)-1])
            print("差分补偿器时间缩放倍率：%s"%self.alpha)
            self.vel = self.vel/self.alpha
            print("更新速度：%s"%self.vel)
            self.acc = self.acc/self.alpha**2
            print("更新加速度：%s"%self.acc)
            self.dec = self.dec/self.alpha**2
            print("更新减速度：%s"%self.dec)
            self.jerk = self.jerk/self.alpha**3
            print("更新Jerk=%s"%self.jerk)
            # 重新进行规划
            self.__profileSpdGen()
            #判断是否存在匀速段
            if disp >= self.__dispCalc():
                # 有匀速段的情况下，直接算出匀速段的持续时间
                self.__Tv = (disp-self.__dispCalc())/self.vel
                # print(self.__Tj1,self.__Ta,self.__Tj1,self.__Tv,self.__Tj2,self.__Td,self.__Tj2)
            else:
                # 没有匀速段的情况下，通过二分法对最大速度进行修改，并重新规划
                self.__binRAMethod(disp,0,self.vel)
            
            res = self.scopeGen()
            #更新总时间大小
            self.total_time = res[4]
            #更新时间轴
            self.time_line = res[0]
            #更新加速度
            self.acc_line = res[2]
            #更新速度
            self.vel_line = res[3]
            #更新jerk
            self.jerk_line = res[1]
                

        #看一下整形器的flag状态
        if self.__ISOn:
            # 开启整形器的话执行整形器和原本信号卷积的程序

            cnva = np.zeros(int(self.CnvT[len(self.CnvT)-1]/self.intval)+1)

            # 如果还打开了自动补偿
            if self.__ISCompOn:
                comp = IS.compensator(self.vel_line)
                comp.Compensate(self.T,self.freq,self.zeta,self.alpha)
                for i in range(len(self.CnvT)):
                    cnva[int(self.alpha*self.CnvT[i]/self.intval)] = self.CnvA[i]
                self.vel_line_shaped = np.convolve(comp.yn,cnva)
                self.vel_line_shaped = self.vel_line_shaped[:len(self.vel_line)]
                self.acc_line_shaped = np.convolve(self.acc_line,cnva)
                self.acc_line_shaped = self.acc_line_shaped[:len(self.acc_line)]
                self.jerk_line_shaped = np.convolve(self.jerk_line,cnva)
                self.jerk_line_shaped = self.jerk_line_shaped[:len(self.jerk_line)]
                print("已使用自动补偿")

            else:
                for i in range(len(self.CnvT)):
                    cnva[int(self.CnvT[i]/self.intval)] = self.CnvA[i]

                self.vel_line_shaped = np.convolve(self.vel_line,cnva)
                self.vel_line_shaped = self.vel_line_shaped[:len(self.vel_line)]
                self.acc_line_shaped = np.convolve(self.acc_line,cnva)
                self.acc_line_shaped = self.acc_line_shaped[:len(self.acc_line)]
                self.jerk_line_shaped = np.convolve(self.jerk_line,cnva)
                self.jerk_line_shaped = self.jerk_line_shaped[:len(self.jerk_line)]


            print("使用整形器,移动了[%s]距离"%disp)
            # print(cnva)
        else:
            print("以[%s]加速度移动了[%s]距离"%(self.acc,disp))

        #计算总位移
        self.disp = []
        sum_disp = 0
        self.disp_shaped = []
        sum_disp_shaped = 0
        for i in self.vel_line:
            self.disp.append(sum_disp)
            sum_disp += i*self.intval
        for i in self.vel_line_shaped:
            self.disp_shaped.append(sum_disp_shaped)
            sum_disp_shaped += i*self.intval





# 虚拟二阶系统
class sec_system:

    def __init__(self,freq,zeta,T) -> None:
        self.omg = freq*2*3.1415927
        self.zeta =zeta
        self.T = T
    def response(self,data):
        yn = []
        yn.append((self.T**2*self.omg**2)*data[0]/(self.T**2*self.omg**2+2*self.T*self.omg*self.zeta + 1))
        yn.append(((self.T**2*self.omg**2)*data[1]-(-2*self.T*self.omg*self.zeta - 2)*yn[0])/(self.T**2*self.omg**2+2*self.T*self.omg*self.zeta + 1))
        for i in range(2,len(data)):
            y = ((self.T**2*self.omg**2)*data[i]-(-2*self.T*self.omg*self.zeta - 2)*yn[i-1]-yn[i-2])/(self.T**2*self.omg**2+2*self.T*self.omg*self.zeta + 1)
            yn.append(y)
        self.yn = yn