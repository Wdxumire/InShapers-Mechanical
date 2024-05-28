# 调用范例
from ProfileGen import *
import InShapers as IS

import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1.inset_locator import mark_inset
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd
import time

# prof = Profile(5248,1613000,1613000,52920000)                        #创建一个运动规划，规定最大速度，加速度，减速度，Jerk
# prof = Profile(10000,50000,50000,1000000)
prof = Profile(3200,60000,60000,1200000)                        #创建一个运动规划，规定最大速度，加速度，减速度，Jerk
# prof = Profile(4638,1260239,1260239,32528769)                        #创建一个运动规划，规定最大速度，加速度，减速度，Jerk

prof.intval_conf(0.001)                                          #设定插补周期(s)
prof.length_conf(400)                                              #设定Scope监视时间(插补周期数)

InShaper = IS.ZVD(45,0.1)                                      #创建一个ZVD整形器
# InShaper = IS.EI(4,0.05)

prof.InShapeOn(InShaper)                                        #开启整形器
# prof.ISCompensateON(0.001,45,0.7) #设置自动差分补偿
prof.ptp(100)                                                   #点对点运动
non_comp_shaped = prof.vel_line_shaped
vel_org = prof.vel_line
acc_org = prof.acc_line
jerk_org = prof.jerk_line
disp_org = prof.disp
prof.ISCompensateON(0.001,45,0.1)                              #设置自动差分补偿
prof.ptp(100)                                                   #点对点运动

# 虚拟二阶系统
sys1 = sec_system(freq=45,zeta=0.001,T=0.001)
sys2 = sec_system(freq=45,zeta=0.001,T=0.001)
sys3 = sec_system(freq=45,zeta=0.001,T=0.001)
sys4 = sec_system(freq=45,zeta=0.001,T=0.001)
sys1.response(vel_org)
sys2.response(prof.vel_line_shaped)
sys3.response(disp_org)
sys4.response(prof.disp_shaped)    

def exportfile(prof:Profile):
    # l = [prof.time_line,prof.vel_line,non_comp_shaped,prof.vel_line_shaped]      
    l = [prof.time_line,prof.vel_line,prof.vel_line_shaped]
    l = list(map(list, zip(*l)))
    output = pd.DataFrame(columns = ['time(s)','acc speed(unit/s)','shaped+comp spd(unit/s)'],data = l)
    output.to_excel('output'+time.strftime('%Y%m%d %H-%M-%S',time.localtime())+'.xlsx',encoding='gbk')

# exportfile(prof) #导出文件

plt.figure(figsize=(10,8))
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=0.3,hspace=0.6)



plt.subplot(321)
plt.grid()
plt.title("速度曲线",y=1,loc="center")
plt.plot(prof.time_line,vel_org)
plt.plot(prof.time_line,prof.vel_line_shaped)
plt.xlabel("时间(s)")
plt.ylabel("速度(unit/s)")

plt.subplot(323)
plt.grid()
plt.title("加速度曲线",y=1,loc="center")
plt.plot(prof.time_line,acc_org)
plt.plot(prof.time_line,prof.acc_line_shaped)
plt.xlabel("时间(s)")
plt.ylabel("加速度(unit/s^2)")

plt.subplot(325)
plt.grid()
plt.title("Jerk曲线",y=1,loc="center")
plt.plot(prof.time_line,jerk_org)
plt.plot(prof.time_line,prof.jerk_line_shaped)
plt.xlabel("时间(s)")
plt.ylabel("Jerk(unit/s^3)")

plt.subplot(324)
plt.grid()
plt.title("速度响应曲线",y=1,loc="center")
plt.plot(prof.time_line,sys1.yn)
plt.plot(prof.time_line,sys2.yn)
plt.xlabel("时间(s)")
plt.ylabel("速度(unit/s)")

plt.subplot(322)
plt.grid()
plt.title("位移曲线",y=1,loc="center")
plt.plot(prof.time_line,disp_org)
plt.plot(prof.time_line,prof.disp_shaped)
plt.xlabel("时间(s)")
plt.ylabel("位移(unit)")

plt.subplot(326)
plt.grid()
plt.title("位移响应曲线",y=1,loc="center")
plt.plot(prof.time_line,sys3.yn)
plt.plot(prof.time_line,sys4.yn)
plt.xlabel("时间(s)")
plt.ylabel("位移(unit)")

print("总规划时间为：",prof.total_time,"s")
print("整形后规划总时间：",prof.total_time+prof.CnvT[len(prof.CnvT)-1]*prof.alpha)

plt.show()
prof.InShapeOff()                                               #关闭整形器