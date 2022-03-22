import sys
import numpy as np
from scipy.interpolate import interp1d

#-----------------------------------------------------
#If you want just to test the code, you can generate an temp array first, for examle:
#b = np.random.uniform(1e2, 1e6, (30, 30, 30))
#np.save('gas_density.npy', b)
#-----------------------------------------------------

#Load simulated data: TEMP, DENS, shock_cells
dens_sim = np.load('gas_density.npy')

option = sys.argv[0]
# = int(input("""Enter the number of the ratio to calculate: \n 1. [S II]/[S II] \n 2. [N II]/Ha \n 3. [O III]/Ha \n 4. [S II]/Ha \n 5. [O III]/Hb \n"""))


#Projection parameter, should ne the same as in main emission calculations!
key = int(sys.argv[1])
# = int(input("Rotation key (from 0 to 2): "))

if key == 0:
        size = np.shape(dens_sim)
        xmin = -3.13421894e+20
        xmax = -7.23281223e+19
elif key == 1:
        dens_sim = np.swapaxes(dens_sim, 0, 1)
        size = np.shape(dens_sim)
        xmin = 2.3e20
        xmax = 5.0e20
else: 
        dens_sim = np.swapaxes(dens_sim, 0, 2)
        size = np.shape(dens_sim)
        xmin = -1.0e20
        xmax = 1.1e20

#Size of the cell
dx = (xmax - xmin)/size[key]

#Absorption cross section is taken from Draine (2003), 
#Silicate Model for Interstellar Dust with R_v = 4.0

if option == 1:
        kappa1 = 6419.0 #SII 6731
        kappa2 = 6419.0 #SII 6731
elif option == 2:
        kappa1 = 6591.8 #N II
        kappa2 = 6693.0 # Ha
elif option == 3:
        kappa1 = 9576.0 #OIII
        kappa2 = 6693.0 # Ha
elif option == 4:
        kappa1 = 6419.0 #SII 6731
        kappa2 = 6693.0 # Ha
else:
        kappa1 = 9576.0 #OIII
        kappa2 = 10010.0 #Hbeta

#Additional one:
#kappa2 = 12870 #SII 4067

dusttogas = 1e-2

tau1 = dens_sim*kappa1*dx*dusttogas
tau2 = dens_sim*kappa2*dx*dusttogas

np.save('tau_emiss1.npy', tau1)
np.save('tau_emiss2.npy', tau2)

print('Tau(z) is ready')