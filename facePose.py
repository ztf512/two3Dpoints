import os
import cv2
import numpy as np
import mediapipe as mp
from two3Dpoints import solve3Dpairs


indices = [1, 2, 9, 10, 33, 58, 93, 127,133, 143,
           168, 195, 263, 288, 323, 356, 362, 372]

reference_vertices = np.array([
	[ 0.000000, -1.126865,  7.475604],  # 1
	[ 0.000000, -2.089024,  6.058267],  # 2
	[ 0.000000,  4.885979,  5.385258],  # 9
	[ 0.000000,  8.261778,  4.481535],  # 10
	[-4.445859,  2.663991,  3.173422],  # 33
	[-6.719682, -4.788645, -1.745401],  # 58
	[-7.542244, -1.049282, -2.431321],  # 93
	[-7.743095,  2.364999, -2.005167],  # 127
	[-1.856432,  2.585245,  3.757904],  # 133
	[-6.407571,  2.236021,  1.560843],  # 143
	[ 0.000000,  3.271027,  5.236015],  # 168
	[ 0.000000,  1.059413,  6.774605],  # 195
	[ 4.445859,  2.663991,  3.173422],  # 263
	[ 6.719682, -4.788645, -1.745401],  # 288
	[ 7.542244, -1.049282, -2.431321],  # 323
	[ 7.743095,  2.364999, -2.005167],  # 356
	[ 1.856432,  2.585245,  3.757904],  # 362
	[ 6.407571,  2.236021,  1.560843]   # 372
])


img_indir = 'images/source'
mp_face_mesh = mp.solutions.face_mesh
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:
	for file in os.listdir(img_indir):
		img_path = os.path.join(img_indir, file)
		img = cv2.imread(img_path)
		H, W = img.shape[:2]
		results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		if not results.multi_face_landmarks:
			print('No face detected.')
			continue
		for face_landmarks in results.multi_face_landmarks:
			target_vertices = []
			for i, lm in enumerate(face_landmarks.landmark):
				if i in indices:
					xyz = [W * lm.x, H *(1 - lm.y), -lm.z * W]
					target_vertices.append(xyz)
			target_vertices = np.array(target_vertices)
			s, R, t = solve3Dpairs(reference_vertices, target_vertices, True, True)
			print(file)
			print('s =', s)
			print('R =\n', R)
			print('t =', t, '\n')
