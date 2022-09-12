import numpy as np


def solve3Dpairs(source: np.ndarray, target: np.ndarray, validation=False, print_loss=False):
    '''
    TODO object function: loss = ||s * R * source + t - target|| ^ 2
         minimize loss, s.t.--> R.T.dot(R) == I and det(R) == 1
         see https://www.math.pku.edu.cn/teachers/yaoy/Fall2011/arun.pdf

    Parameters:
        source: [[xs0, ys0, zs0], [xs1, ys1, zs1], ..., [xsn-1, ysn-1, zsn-1]], (n, 3)
        target: [[xt0, yt0, zt0], [xt1, yt1, zt1], ..., [xtn-1, ytn-1, ztn-1]], (n, 3)
    Returns:
        s:  scalar, scaling coefficient
        R: ndarray, rotation matrix,    (3, 3)
        t: ndarray, translation vector, (3,)
    '''

    center_source = source.mean(axis=0)
    std_source = source - center_source
    mean_scale_source = np.sqrt(np.sum(std_source ** 2, axis=1)).mean()
    std_source = std_source / mean_scale_source

    center_target = target.mean(axis=0)
    std_target = target - center_target
    mean_scale_target = np.sqrt(np.sum(std_target ** 2, axis=1)).mean()

    s = mean_scale_target / mean_scale_source
    target /= s
    center_target = target.mean(axis=0)
    std_target = target - center_target

    H = std_source.T.dot(std_target)
    U, sigma, VT = np.linalg.svd(H)
    R = VT.T.dot(U.T)
    t = s * (center_target - R.dot(center_source))

    if validation:
        if abs(np.linalg.det(R) - 1) < 1e-8:
            print('SVD solving succeeded.')
        else:
            inv = np.eye(3)
            inv[2, 2] = -1
            R = VT.T.dot(inv).dot(U.T)

    if print_loss:
        loss = np.sum((s * source.dot(R.T) + t - s * target) ** 2)
        print('loss =', loss)

    return s, R, t


if __name__ == '__main__':
    pts1 = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 2, 0],
        [0, 0, 3]
    ])

    scale = 100
    theta = np.pi / 2
    rm = np.array([
        [ np.cos(theta), 0, np.sin(theta)],
        [             0, 1,             0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])                                      # rotate around the y-axis
    offset = np.array([1, 23, 456])

    print('s gt:\n', scale)
    print('R gt:\n', rm)
    print('t gt:\n', offset, '\n')

    noise = np.random.randn(*pts1.shape) * 0.1
    pts2 = scale * pts1.dot(rm.T) + offset + noise
    s, r, t = solve3Dpairs(pts1, pts2, validation=True, print_loss=True)

    print('\ns pred:\n', s)
    print('R pred:\n', r)
    print('t pred:\n',t)
