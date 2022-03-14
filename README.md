# CESS
CESS: Cooling Emission in the optical band from Supernovae in MHD Simulations

A post-processing module for the FLASH code calculates the cooling radiation in optical bands.
Based on collisional data from MAPPINGS V code (cooling tables are included).
Note: here is only a calculation of line ratios, but you can easily use it to get flux maps in isolated optical filters.

You can calculate the following line ratios:
1. [S II] 6717 /[S II] 6731
2. [N II] 6583 / Ha 6365
3. [O III] 5007 /Ha 6563
4. [S II] 6731 / Ha 6563
5. [O III] 6731 / Hb 4861

The structure is:
1. emiss_3Dcube.py - calculates the cooling emission cube using the temperature 3D cube from simulations from the MAPPINGS V tables.
2. tau.py - if you want to take into account dust attenuation within the cube, calculates tau cube (using absorption cross-section from Draine (2003))
3. rt.py - project your 3D cube to 2D taking into account a simple radiative transfer.
You can see more details on the attached diagram for the step-by-step procedure.
