import sys
import numpy as np
from scipy.interpolate import interp1d

#-----------------------------------------------------
#If you want just to test the code, you can generate an temp array first, for examle:
#b = np.random.uniform(1e2, 1e6, (30, 30, 30))
#np.save('gas_density.npy', b)
#-----------------------------------------------------

#Load simulated data: DENS
dens_sim = np.load('gas_density.npy')

#option = sys.argv[1]
option = int(input("""Enter the number of the ratio to calculate: \n 1. [S II]/[S II] \n 2. [N II]/Ha \n 3. [O III]/Ha \n 4. [S II]/Ha \n 5. [O III]/Hb \n"""))

#n = len(sys.argv[2])
#coord = sys.argv[2][0:n-1]
#coord = coord.split(',')
#Put in your coordinates is cm: [xmin, xmax, ymin, ymax, zmin, zmax]
coord = [-2.9e+20,-0.9e+20, 2.3e+20, 5e+20, -1.0e+20, 1.1e+20]

#Projection parameter, should ne the same as in main emission calculations!
#key = int(sys.argv[3])
key = int(input("Rotation key (from 0 to 2): "))

if key == 0:
        size = np.shape(dens_sim)
        xmin = float(coord[0])
        xmax = float(coord[1])
elif key == 1:
        dens_sim = np.swapaxes(dens_sim, 0, 1)
        size = np.shape(dens_sim)
        xmin = float(coord[2])
        xmax = float(coord[3])
elif key == 2: 
        dens_sim = np.swapaxes(dens_sim, 0, 2)
        size = np.shape(dens_sim)
        xmin = float(coord[4])
        xmax = float(coord[5])

#Size of the cell
dx = (xmax - xmin)/size[key]

# The dust absorption cross-section is taken from Weingartner & Draine (2001): 
# we use the silicate model for Interstellar Dust for Milky Way with R_V = 4.0.

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
elif option == 5:
        kappa1 = 9576.0 #OIII
        kappa2 = 10010.0 #Hbeta

#Additional one:
#kappa2 = 12870 #SII 4067

#Constant from the simulations:
dusttogas = 1e-2

tau1 = dens_sim*kappa1*dx*dusttogas
tau2 = dens_sim*kappa2*dx*dusttogas

np.save('tau_emiss1.npy', tau1)
np.save('tau_emiss2.npy', tau2)

print('Tau(z) is ready')
