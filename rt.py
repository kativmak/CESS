import sys
import numpy as np

#Projection parameter, should be the same as in the main emission calculations!
key = int(sys.argv[1])
#int(input("Rotation key (from 0 to 2): "))

#Choose the line raion:
option = int(sys.argv[2])

#If bg == 0 there is no background subtraction; 
#if bg == 1, you need to calculate background arrays for each line using emiss_3Dcube.py
bg = int(sys.argv[3])

n = len(sys.argv[4])
coord = sys.argv[4][0:n-1]
coord = coord.split(',')

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
	if option == 4:
		emiss_1unr = np.load('emiss_1_unres.npy')
elif bg == 1:
	emiss_bg_1 = np.load('bg_emiss_1.npy')
	emiss_bg_2 = np.load('bg_emiss_2.npy')
	if option == 4:
		emiss_bg_1unr = np.load('bg_emiss_1_unres.npy')
	emiss_1 = np.load('emiss_1.npy')
	emiss_2 = np.load('emiss_2.npy')
	emiss_1 = emiss_1 - emiss_bg_1
	emiss_1[emiss_1 < 0.0] = 0.0
	emiss_2 = emiss_2 - emiss_bg_2
	emiss_2[emiss_2 < 0.0] = 0.0
	if option == 4:		
		emiss_1_unr = emiss_1unr - emiss_bg_1unr
		emiss_1_unr[emiss_1_unr < 0.0] = 0.0
		
#Right side of the cube
emiss1_1 = np.flip(emiss_1, 1)
emiss2_1 = np.flip(emiss_1, 0)
emiss1_2 = np.flip(emiss_2, 1)
emiss2_2 = np.flip(emiss_2, 0)
if option == 4:
	emiss1_1unr = np.flip(emiss_1unr, 1)
	emiss2_1unr = np.flip(emiss_1unr, 0)

#Projection: rotate an array (1-3)
if key == 0:
	xmin = float(coord[0])
	xmax = float(coord[1])
if key == 1:
	xmin = float(coord[2])
	xmax = float(coord[3])
else:
	xmin = float(coord[4])
	xmax = float(coord[5])

size = np.shape(emiss_1)
dx = (xmax - xmin)/size[(key)]

for i in range(size[key]):
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

if option == 4:
	for i in range(size[key]):
		if i == 0:
			integ_em_1unr = emiss_1unr[0]* np.exp(-tau_1[0])*1e21*1e22/dx/dx #bottom from the top of the cube
			integ_em_rev_1unr = emiss2_1unr[0]*np.exp(-tau2_1[0])*1e21*1e22/dx/dx #bottom of the cube
		else:
			tau_1[i] = tau_1[i] + tau_1[i-1]
			tau2_1[i] = tau2_1[i] + tau2_1[i-1]
			integ_em_1unr += emiss_1unr[i]  * np.exp(-tau_1[i])*1e21*1e22/dx/dx
			integ_em_rev_1unr += emiss2_1unr[i]  * np.exp(-tau2_1[i])*1e21*1e22/dx/dx


#Fixing the 'resolution'(/arcsec^2 )
integ_em_2 = integ_em_2/35.0/size[key]
integ_em_1 = integ_em_1/35.0/size[key]
integ_em_rev_1 = integ_em_rev_1/35.0/size[key]
integ_em_rev_2 = integ_em_rev_2/35.0/size[key]

if option == 4:
	integ_em_1unr = integ_em_1unr/35.0/size[key]
	integ_em_rev_1unr = integ_em_rev_1unr/35.0/size[key]

#np.save('em_1', integ_em_1)
#np.save('em_2', integ_em_2)
#np.save('em_rev_1', integ_em_rev_1)
#np.save('em_rev_2', integ_em_rev_2)

#Calculation of the mean for resolved SNR
integ_em_2[integ_em_2 < 3e-18] = 1e20
integ_em_1[integ_em_1 < 3e-18] = 0.0
integ_em_rev_1[integ_em_rev_1 < 3e-18] = 0.0
integ_em_rev_2[integ_em_rev_2 < 3e-18] = 1e20
mean_1 = integ_em_1/integ_em_2
mean_2 = integ_em_rev_1/integ_em_rev_2
mean1 = np.mean(mean_1[mean_1 != 0.0])
mean2 = np.mean(mean_2[mean_2 != 0.0])
file = open('result_res_snr.txt', 'a')
file.write(str(mean1) + ' ' + str(mean2) + '\n')
file.close()

#Calculation of the mean for unresolved SNR
if option == 4:
	integ_em_1unr[integ_em_1unr < 3e-18] = 0.0
	integ_em_rev_1unr[integ_em_rev_1unr < 3e-18] = 0.0
	integ_em_2[integ_em_2 == 1e20] = 0.0
	integ_em_rev_2[integ_em_rev_2 == 1e20] = 0.0
	mean1 = np.sum(integ_em_1unr)/np.sum(integ_em_2)
	mean2 = np.sum(integ_em_rev_1unr)/np.sum(integ_em_rev_2)
	file = open('result_unres_snr.txt', 'a')
	file.write(str(mean1) + ' ' + str(mean2) + '\n')
	file.close()
else:
	integ_em_2[integ_em_2 == 1e20] = 0.0
	#integ_em_1[integ_em_1 < 3e-18] = 0.0
	#integ_em_rev_1[integ_em_rev_1 < 3e-18] = 0.0
	integ_em_rev_2[integ_em_rev_2 == 1e20] = 0.0
	mean1 = np.sum(integ_em_1)/np.sum(integ_em_2)
	mean2 = np.sum(integ_em_rev_1)/np.sum(integ_em_rev_2)
	file = open('result_unres_snr.txt', 'a')
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
