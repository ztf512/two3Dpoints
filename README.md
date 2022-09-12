# two3Dpoints
## 1. Introduction
Solving for rigid transformation parameters for two sets of 3D points.\
English see [here](README_EN.md).

求解两组3D顶点source与target之间的刚性变换参数，包括缩放系数*s*、旋转矩阵*R*、平移向量*t*。**注意source与target的顶点序号必须是一一对应的**，可以认为是顶点对应关系已知+带缩放变换的简易版ICP算法。target由source经过以下变换得到：
$$target = sRsource + t$$
参考[这篇论文](https://www.math.pku.edu.cn/teachers/yaoy/Fall2011/arun.pdf)，通过最小二乘拟合求解以下优化问题：
$$minimize\quad \left|\left|sRsource + t - target\right|\right|_2^2,$$
$$subject\ to\quad R^TR = I,\ det(R) = 1$$
使用SVD进行求解。当传入**四对及以上不共面**的3D点对时，该问题具有唯一闭式解，SVD求解结果不需要进行验证。
## 2. 使用示例——求解人脸姿态角
使用[mediapipe Face Mesh](https://github.com/google/mediapipe)获取人脸3D关键点target，在[基准人脸](canonical_face_model)中选取若干3D点作为source，利用solve3Dpairs进行求解，见[这里](facePose.py)。\
利用求解到的*s*、*R*、*t*对[face_model.obj](canonical_face_model/face_model.obj)进行刚性变换，然后利用简易渲染程序将基准3D人脸投影至原图片上，结果如下：\
![result0](images\result\Trump0_result.png)
![result1](images\result\Trump1_result.png)
![result2](images\result\Trump2_result.png)
