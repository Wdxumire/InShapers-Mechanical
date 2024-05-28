# 输入整形算法的Python实现

输入整形最早出现在多轴机器人的设计上，某些机械执行机构的末端具有柔性结构和负载，在机械停止时由于自身模态产生了残留振动，导致末端精度降低，并影响其快速定位能力。

为了解决这个问题，利用末端残留振动产生的原理，在控制信号端加入一个滤波器，这个滤波器实际上就是整形器，通过整形器的整形实现末端残留振动的控制。

该脚本建立了InShapers类库和ProfileGen类库，分别是整形器类和规划生成类：

### Main.py

主程序，这里包括了一个可用范例。
1. 设定运动规划：ProfileGen.Profile()；
2. 设定整形器； 
3. 实行点对点运动ptp；
4. 绘图处理结果。


### InShapers.py

放到项目目录下，引用:
```python
import InShapers as IS
```
IS包含下列的整形器
- ZV
- ZVD
- ZVDD
- ZVDDD
- MISZV
- EI
- H2EI
- H3EI

每种整形器的参数都不一样，详情见代码。

### ProfileGen.py

包含了一个Profile对象，该对象的实例化方法：
```python
from ProfileGen import *
prof = Profile(3200,60000,60000,1200000)
```
依次填写速度，加速度，减速度，Jerking。基础长度单位unit，基础时间单位s。

`ptp(disp:float,int)`  

按照设定好的运动规划移动disp距离。


`intval_conf(intval:float)` 

设定插补周期，单位为s。

`length_conf(length:int)`

设定要分析的信号总长度点数。

`InShapeOn(obj:InShape)`、`InShapeOFF()`

开启和关闭整形器。

`ISCompensateON(T,freq,zeta)`、`ISCompensateOFF()`

开启和关闭补偿器，补偿器是一种消除整形器带来延时的一种改进机制，但是实际场合上实现起来较为困难。
T为离散插值周期，单位s；freq表示为目标固有频率，单位Hz；zeta为阻尼比。

## 许可证

包含MIT许可证