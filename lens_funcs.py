import numpy as np

#field of view from a width and focal length
def fov(fl, w):
    return 2*math.atan2(w/2, fl)

#handy functions to create ray transfer matricies
def f_mat(fl):
    return np.array([[1.0, 0.0],[-1.0/fl, 1.0]])
def d_mat(dist):
    return np.array([[1.0, dist],[0.0, 1.0]])


#microlens array focused on an imager
def pix_to_rayvec(pixnum, num_pix, pitch, ml_pitch, ml_f):
    x = (pixnum-num_pix/2 + 0.5)*pitch
    ml = round(x/ml_pitch)
    ml_x = ml*ml_pitch
    slope = (x-ml_x)/ml_f
    return np.array([[ml_x],[slope]])

def rayvec_to_pix(rayvec, imager_h, pitch=pix_pitch, ml_pitch=mla_pitch, ml_f=mla_f):
    x, slope = rayvec.reshape(2)
    ml = round(x/ml_pitch)
    ml_x = ml*ml_pitch
    pix_x = slope*ml_f + ml_x
    pixnum = int(round((pix_x + imager_h/2) / pitch))
    return pixnum
