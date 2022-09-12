# two3Dpoints
## 1. Introduction
Solving for rigid transformation parameters for two sets of 3D points.

Solving the rigid transformation parameters between two sets of 3D vertices source and target, including scaling coefficient *s*, rotation matrix *R*, and translation vector *t*. **Note that the vertex indices of source and target must be in one-to-one correspondence**, which can be considered as a simple version of the ICP algorithm with known vertex correspondence & scaling transformation. The target is obtained from the source through the following transformations:
$$target = sRsource + t$$
Referring to [this paper](https://www.math.pku.edu.cn/teachers/yaoy/Fall2011/arun.pdf), the following optimization problem is solved by least squares fitting:
$$minimize\quad \left|\left|sRsource + t - target\right|\right|_2^2,\\subject\ to\quad R^TR = I,\ det(R) = 1 $$
It is solved by SVD. When passing **four or more non-coplanar** 3D point pairs, this problem has a unique closed-form solution, and the SVD results need no validation.
## 2. Example: Solving Face Pose
Use [mediapipe Face Mesh](https://github.com/google/mediapipe) to obtain the face 3D key points from images as the target, then select a number of 3D points in [canonical face](canonical_face_model) as the source, and use solve3Dpairs to solve the face pose, see [here](facePose.py).\
Use the solved *s*, *R*, *t* to perform rigid transformation on [face_model.obj](canonical_face_model/face_model.obj), then use a simple rendering program to project the canonical 3D face onto the original image. The results are as follows: \
![result0](images\result\Trump0_result.png)
![result1](images\result\Trump1_result.png)
![result2](images\result\Trump2_result.png)
