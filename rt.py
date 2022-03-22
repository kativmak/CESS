import sys
import numpy as np

#Projection parameter, should ne the same as in main emission calculations!
key = sys.argv[0]
#int(input("Rotation key (from 0 to 2): "))
res_opt = int(sys.argv[1])
#int(input("Resolved (0) or unresolved (1) SNR calculations?: "))
bg = int(sys.argv[2])

#Optical depth files loading
tau_1 = np.load('tau_emiss1.npy')
tau_2 = np.load('tau_emiss2.npy')

#Right side of the cube
tau1_1 = np.flip(tau_1, 1)
tau2_1 = np.flip(tau_1, 0)
tau1_2 = np.flip(tau_2, 1)
tau2_2 = np.flip(tau_2, 0)

#Emission files loading
if bg == 0:
	emiss_1 = np.load('emiss_1.npy')
	emiss_2 = np.load('emiss_2.npy')
elif bg == 1:
	emiss_bg_1 = np.load('bg_emiss_1.npy')
	emiss_bg_2 = np.load('bg_emiss_2.npy')
	emiss_1 = np.load('emiss_1.npy')
	emiss_2 = np.load('emiss_2.npy')
	emiss_1 = emiss_1 - emiss_bg_1
	emiss_1[emiss_1 < 0.0] = 0.0
	emiss_2 = emiss_2 - emiss_bg_2
	emiss_2[emiss_2 < 0.0] = 0.0

#Right side of the cube
emiss1_1 = np.flip(emiss_1, 1)
emiss2_1 = np.flip(emiss_1, 0)
emiss1_2 = np.flip(emiss_2, 1)
emiss2_2 = np.flip(emiss_2, 0)

#Projection: rotate an array (1-3)
if key == 0:
	xmin = -3.13421894e+20
	xmax = -7.23281223e+19
if key == 1:
	xmin = 2.3e20
	xmax = 5.0e20
else:
	xmin = -1.0e20
	xmax = 1.1e20

size = np.shape(emiss_1)
dx = (xmax - xmin)/size[(0)]

for i in range(size[0]):
	if i == 0:
		integ_em_1 = emiss_1[0]* np.exp(-tau_1[0])*1e21*1e22/dx/dx #bottom from the top of the cube
		integ_em_rev_1 = emiss2_1[0]*np.exp(-tau2_1[0])*1e21*1e22/dx/dx #bottom of the cube
		integ_em_2 = emiss_2[0]* np.exp(-tau_2[0])*1e21*1e22/dx/dx
		integ_em_rev_2 = emiss2_2[0]*np.exp(-tau2_2[0])*1e21*1e22/dx/dx
	else:
		tau_1[i] = tau_1[i] + tau_1[i-1]
		tau2_1[i] = tau2_1[i] + tau2_1[i-1]
		integ_em_1 += emiss_1[i]  * np.exp(-tau_1[i])*1e21*1e22/dx/dx
		integ_em_rev_1 += emiss2_1[i]  * np.exp(-tau2_1[i])*1e21*1e22/dx/dx
 		tau_2[i] = tau_2[i] + tau_2[i-1]
		tau2_2[i] = tau2_2[i] + tau2_2[i-1]
		integ_em_2 += emiss_2[i] * np.exp(-tau_2[i])*1e21*1e22/dx/dx
		integ_em_rev_2 += emiss2_2[i] * np.exp(-tau2_2[i])*1e21*1e22/dx/dx

#Fixing the 'resolution'(/arcsec^2 )
integ_em_2 = integ_em_2/35.0/size[0]
integ_em_1 = integ_em_1/35.0/size[0]
integ_em_rev_1 = integ_em_rev_1/35.0/size[0]
integ_em_rev_2 = integ_em_rev_2/35.0/size[0]

#np.save('em_1', integ_em_1)
#np.save('em_2', integ_em_2)
#np.save('em_rev_1', integ_em_rev_1)
#np.save('em_rev_2', integ_em_rev_2)

if res_opt == 0:
	integ_em_2[integ_em_2 < 3e-18] = 1e20
	integ_em_1[integ_em_1 < 3e-18] = 0.0
	integ_em_rev_1[integ_em_rev_1 < 3e-18] = 0.0
	integ_em_rev_2[integ_em_rev_2 < 3e-18] = 1e20
	mean_1 = integ_em_1/integ_em_2
	mean_2 = integ_em_rev_1/integ_em_rev_2
	mean1 = np.mean(mean_1[mean_1 != 0.0])
	mean2 = np.mean(mean_2[mean_2 != 0.0])
elif res_opt == 1:
	integ_em_2[integ_em_2 < 3e-18] = 0.0
	integ_em_1[integ_em_1 < 3e-18] = 0.0
	integ_em_rev_1[integ_em_rev_1 < 3e-18] = 0.0
	integ_em_rev_2[integ_em_rev_2 < 3e-18] = 0.0
	mean1 = np.sum(integ_em_1)/np.sum(integ_em_2)
	mean2 = np.sum(integ_em_rev_1)/np.sum(integ_em_rev_2)

file = open('res.txt', 'a')
file.write(str(mean1) + ' ' + str(mean2) + '\n')
file.close()

#Observ. limit
#3 *10^{-18} erg/s/cm^2/arcsec^2
#for LVM targeting the Milky Way at 37"~ pc scales, 3 sigma sensitivity;
#integ_em_2[integ_em_2 < 3e-18] = 0.0 # == 0.0 in general case. If you want to do a res. SNR use 1e20
#integ_em_1[integ_em_1 < 3e-18] = 0.0
#integ_em_rev_1[integ_em_rev_1 < 3e-18] = 0.0
#integ_em_rev_2[integ_em_rev_2 < 3e-18] = 0.0 # the same as above



print('RT is done and all arrays are saved')