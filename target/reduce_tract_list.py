import pyfits as pf
import numpy as np

d = pf.open("tract_list_wide.fits")[1].data
tract = d["tract"]
tract_list = np.sort(np.array(list(set(tract))))

np.savetxt("tract_list_wide.txt", tract_list, fmt="%i")



d = pf.open("tract_list_dud.fits")[1].data
tract = d["tract"]
tract_list = np.sort(np.array(list(set(tract))))

np.savetxt("tract_list_dud.txt", tract_list, fmt="%i")
