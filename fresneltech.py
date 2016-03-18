import numpy as np
import lens_funcs as lf
import math
import lytro_optics as lytro


#microlenses cover ~10 pixels in width
mla_pitch = 1e-3 #(m)
mla_num_lenses = 150 #along one axis, for a 6inx6in sheet
mla_f = 3e-3 #(m)
mla_fnum = mla_f/mla_pitch
mla_fov = lf.fov(mla_f, mla_pitch)

#do the lytro reverse model
lytro_mla_rays = np.column_stack([lytro.pix_to_rayvec(p) for p in range(lytro.num_pix)]).T
lytro_mla_aperture = lytro_mla_rays[-1, 0] - lytro_mla_rays[0, 0]
lytro_mla_fov = math.atan(lytro_mla_rays.max(0)[1]) - math.atan(lytro_mla_rays.min(0)[1])

lytro_out_rays = np.column_stack([lytro.lytro_proj_mat.dot(ray) for ray in lytro_mla_rays]).T
lytro_out_aperture = lytro_out_rays[-1, 0] - lytro_out_rays[0, 0]
lytro_out_fov = math.atan(lytro_out_rays.max(0)[1]) - math.atan(lytro_out_rays.min(0)[1])

# pretend we put 10px behind each microlens
pix_per_lens = 10
num_pix = mla_num_lenses * pix_per_lens
pix_pitch = mla_pitch / pix_per_lens
def pix_to_rayvec(pixnum):
    return lf.pix_to_rayvec(pixnum, num_pix, pix_pitch, mla_pitch, mla_f)
def rayvec_to_pix(rayvec):
    return lf.rayvec_to_pix(rayvec, imager_h, pix_pitch, mla_pitch, mla_f)

src_rays = np.column_stack([lytro.pix_to_rayvec(p) for p in range(lytro.num_pix)]).T
src_aperture = src_rays[-1, 0] - src_rays[0, 0]
src_fov = math.atan(src_rays.max(0)[1]) - math.atan(src_rays.min(0)[1])

#we want to put a lens in front of the mla to make the output approximately the same as the input to the lytro
#focal length
f = -100e-3

def try_lens(f, d=None, rays=src_rays):
    if not d:
        d = abs(f)
    #model main lens as thin lens focusing on microlens array at f
    lens_mat = lf.d_mat(d).dot(lf.f_mat(f))
    #reverse lens to project from a microlens into the real world
    proj_mat = lf.f_mat(f).dot(lf.d_mat(d))

    out_rays = np.column_stack([proj_mat.dot(ray) for ray in rays]).T
    out_aperture = out_rays[-1, 0] - out_rays[0, 0]
    out_fov = math.atan(out_rays.max(0)[1]) - math.atan(out_rays.min(0)[1])
    return out_aperture, out_fov, out_rays
