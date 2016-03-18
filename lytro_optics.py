import numpy as np
import lens_func as lf
import math


#imager is MT9F002 (http://www.onsemi.com/pub_link/Collateral/MT9F002-D.PDF)
#3288x3288 center section is all the lytro uses
pix_pitch = 1.4e-6 #m/pix from datasheet
pix_pitch = 0.000001399999976158141876680929 #(m/pix) from lytro config
num_pix = 3280
imager_w = num_pix*pix_pitch
imager_h = num_pix*pix_pitch
#35mm diagonal is 43.3mm
crop_factor = 43.3e-3/math.sqrt(imager_w**2 + imager_h**2)
#microlenses cover ~10 pixels in width
mla_pitch = 10*pix_pitch
mla_pitch = 0.000013898599624633789417771368 #(m) from lytro config
mla_fnum = 1.90999996662139892578125 #pretend mla fnum == main lens fnum
mla_f = mla_fnum*mla_pitch
mla_fov = lf.fov(mla_f, mla_pitch)

def pix_to_rayvec(pixnum):
    return lf.pix_to_rayvec(pixnum, num_pix, num_pix, pitch, ml_pitch, ml_f)
def rayvec_to_pix(rayvec):
    return lf.rayvec_to_pix(rayvec, imager_h, pitch, ml_pitch, ml_f)

#focal length
#range is 43-344mm (https://support.lytro.com/hc/en-us/articles/200863400-What-are-the-specs-on-the-First-Generation-Lytro-Light-Field-Camera-)
f = 43e-3
#on further note, that might be a 35mm equivalent
f = f/crop_factor
f = 0.006440000057220458984375 #from lytro config
#see here: http://optics.miloush.net/lytro/TheCamera.aspx
#f = 28.1e-3
lytro_fov = lf.fov(f, imager_w)

#model lytro main lens as thin lens focusing on microlens array at f
lytro_lens_mat = lf.d_mat(f).dot(lf.f_mat(f))
#reverse lytro lens to project from a microlens into the real world
lytro_proj_mat = lf.f_mat(f).dot(lf.d_mat(f))
