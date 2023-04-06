import sys
import numpy as np
from scipy.interpolate import interp1d
from itertools import product
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LogNorm, Normalize

#-----------------------------------------------------
#If you want just to test the code, you can generate an temp array first, for examle:
#b = np.random.uniform(1e2, 1e6, (30, 30, 30))
#np.save('gas_temp.npy', b)
#-----------------------------------------------------

#file_numb = sys.argv[1]
file_numb = int(input("# of the snapshot: "))

#option = int(sys.argv[2])
option = int(input("""Enter the number of the ratio to calculate: \n 1. [S II]/[S II] \n 2. [N II]/Ha \n 3. [O III]/Ha \n 4. [S II]/Ha \n 5. [O III]/Hb \n"""))

#bg = int(sys.argv[3])
bg = int(input("""Is it a background emission calculations? \n 1. Yes \n 2. No \n"""))
#key = int(sys.argv[4])
key = int(input("Rotation key (from 0 to 2): "))

h_star = 3.086e18 #pc -> cm

#load the emission data
if option == 1:
	emis_1 = np.fromfile('./MV_tables/s2_solar/s6731.dat', dtype=float, count=-1, sep='\n')
	hbeta_1 = np.fromfile('./MV_tables/s2_solar/hbeta_6731.dat', dtype=float, count=-1, sep='\n')
	temp_1 = np.fromfile('./MV_tables/s2_solar/temp_6731.dat', dtype=float, count=-1, sep='\n')
	emis_2 = np.fromfile('./MV_tables/s2_solar/s6717.dat', dtype=float, count=-1, sep='\n')
	hbeta_2 = np.fromfile('./MV_tables/s2_solar/hbeta_6717.dat', dtype=float, count=-1, sep='\n')
	temp_2 = np.fromfile('./MV_tables/s2_solar/temp_6717.dat', dtype=float, count=-1, sep='\n')
elif option == 2:
	emis_1 = np.fromfile('./MV_tables/n2_solar/n2.dat', dtype=float, count=-1, sep='\n')
	hbeta_1 = np.fromfile('./MV_tables/n2_solar/hb.dat', dtype=float, count=-1, sep='\n')
	temp_1 = np.fromfile('./MV_tables/n2_solar/temp.dat', dtype=float, count=-1, sep='\n')
	emis_2 = np.fromfile('./MV_tables/ha_full/ha.dat', dtype=float, count=-1, sep='\n')
	hbeta_2 = np.fromfile('./MV_tables/ha_full/hb.dat', dtype=float, count=-1, sep='\n')
	temp_2 = np.fromfile('./MV_tables/ha_full/temp.dat', dtype=float, count=-1, sep='\n')
elif option == 3:
	emis_1 = np.fromfile('./MV_tables/o3_solar/o3.dat', dtype=float, count=-1, sep='\n')
	hbeta_1 = np.fromfile('./MV_tables/o3_solar/hbeta.dat', dtype=float, count=-1, sep='\n')
	temp_1 = np.fromfile('./MV_tables/o3_solar/temp.dat', dtype=float, count=-1, sep='\n')
	emis_2 = np.fromfile('./MV_tables/ha_full/ha.dat', dtype=float, count=-1, sep='\n')
	hbeta_2 = np.fromfile('./MV_tables/ha_full/hb.dat', dtype=float, count=-1, sep='\n')
	temp_2 = np.fromfile('./MV_tables/ha_full/temp.dat', dtype=float, count=-1, sep='\n')
elif option == 4:
	emis1_2 = np.fromfile('./MV_tables/s2_solar/s6717.dat', dtype=float, count=-1, sep='\n')
	hbeta1_2 = np.fromfile('./MV_tables/s2_solar/hbeta_6717.dat', dtype=float, count=-1, sep='\n')
	temp1_2 = np.fromfile('./MV_tables/s2_solar/temp_6717.dat', dtype=float, count=-1, sep='\n')
	emis_1 = np.fromfile('./MV_tables/s2_solar/s6731.dat', dtype=float, count=-1, sep='\n')
	hbeta_1 = np.fromfile('./MV_tables/s2_solar/hbeta_6731.dat', dtype=float, count=-1, sep='\n')
	temp_1 = np.fromfile('./MV_tables/s2_solar/temp_6731.dat', dtype=float, count=-1, sep='\n')
	emis_2 = np.fromfile('./MV_tables/ha_full/ha.dat', dtype=float, count=-1, sep='\n')
	hbeta_2 = np.fromfile('./MV_tables/ha_full/hb.dat', dtype=float, count=-1, sep='\n')
	temp_2 = np.fromfile('./MV_tables/ha_full/temp.dat', dtype=float, count=-1, sep='\n')
elif option == 5:
	emis_1 = np.fromfile('./MV_tables/o3_solar/o3.dat', dtype=float, count=-1, sep='\n')
	hbeta_1 = np.fromfile('./MV_tables/o3_solar/hbeta.dat', dtype=float, count=-1, sep='\n')
	temp_1 = np.fromfile('./MV_tables/o3_solar/temp.dat', dtype=float, count=-1, sep='\n')
	#emis_2 = np.fromfile('./MV_tables/ha_full/ha.dat', dtype=float, count=-1, sep='\n')
	hbeta_2 = np.fromfile('./MV_tables/ha_full/hb.dat', dtype=float, count=-1, sep='\n')
	temp_2 = np.fromfile('./MV_tables/ha_full/temp.dat', dtype=float, count=-1, sep='\n')

#Note that emission is normalized on hbeta, so we first multiply on hbeta
emis_1 = emis_1*hbeta_1

#for unres SNRs:
if option == 4:
	emis1_2 = emis1_2*hbeta1_2
	interp_func1_2 = interp1d(temp1_2, emis1_2)
if option == 5:
	emis_2 = hbeta_2
else:
	emis_2 = emis_2*hbeta_2

#Load simulation data: TEMP array
temp_sim = np.load('gas_temp.npy')
print('TEMP shape:', np.shape(temp_sim))

#Choosing the projection view: rotate an array (1-3)
if key == 0:
	size = np.shape(temp_sim)
elif key == 1:
	temp_sim = np.swapaxes(temp_sim, 0, 1)
	size = np.shape(temp_sim)
elif key == 2:
	temp_sim = np.swapaxes(temp_sim, 0, 2)
	size = np.shape(temp_sim)

#Define the temp limits for the emission
low_lim1 = temp_1[0]
up_lim1 = temp_1[-1]
low_lim2 = temp_2[0]
up_lim2 = temp_2[-1]

#Interpolation itself
emiss_1 = np.where((low_lim1  < temp_sim) & (temp_sim < up_lim1), np.interp(temp_sim, temp_1, emis_1), 0.0)
emiss_2 = np.where((low_lim2  < temp_sim) & (temp_sim < up_lim2), np.interp(temp_sim, temp_2, emis_2), 0.0)

print('Min and max for the first emission: ', np.amin(emiss_1), np.amax(emiss_1))
print('Min and max for the second emission: ', np.amin(emiss_2), np.amax(emiss_2))

#Let's save the data
if bg == 1:
	np.save('bg_emiss_1.npy', emiss_1)
	np.save('bg_emiss_2.npy', emiss_2)
elif bg == 0:
	np.save('emiss_1.npy', emiss_1)
	np.save('emiss_2.npy', emiss_2)

if option == 4:
	emiss1_2 = np.where((temp1_2[0]  < temp_sim) & (temp_sim < temp1_2[-1]), np.interp(temp_sim, temp1_2, emis1_2), 0.0)
	emiss_1 = emiss_1 + emiss1_2

	#Let's save the data
	if bg == 1:
		np.save('bg_emiss_1_unres.npy', emiss_1)
	elif bg == 0:
		np.save('emiss_1_unres.npy', emiss_1)

print('Emission cubes are ready')
