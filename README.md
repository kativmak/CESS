# CESS
CESS: Cooling Emission in the optical band from Supernovae in (M)HD Simulations

A post-processing module for the FLASH simulations that calculates the cooling radiation from the supernovae in forbidden optical lines.
Based on collisional data from MAPPINGS V code (cooling tables are included). Note, photoionisation process is not included. The gas is assumed to be in collisional ionisation equilibrium (CIE).

You can calculate the following line ratios:
1. [S II] 6717 /[S II] 6731
2. [N II] 6583 / Ha 6365
3. [O III] 5007 /Ha 6563
4. [S II] 6731 / Ha 6563
5. [O III] 6731 / Hb 4861

The structure is following:
1. emiss_3Dcube.py - calculates the cooling emission cube using the temperature 3D cube from simulations from the MAPPINGS V tables.
2. tau.py - if you want to take into account dust attenuation within the supernovae cube, calculates tau cube (using absorption cross-section from Draine (2003))
3. rt.py - project your 3D cube to 2D taking into account a simple radiative transfer.
You can see more details on the attached diagram for the step-by-step procedure.
As a default, there is only a calculation of line ratios, but you can easily use it to get flux maps in isolated optical filters.

To start CESS you need to have uniform grid data (not an AMR-grid). You can use this tool to reproject your data to the uniform grid: 
https://bitbucket.org/pierrenbg/flash-amr-tools/src/master/

Other details & results can be found in  [} Makarenko, E.I., Walch, S., Clarke, S.D., et al. 2020, Journal of Physics Conference Series, 1640, 012009. doi:10.1088/1742-6596/1640/1/012009
](https://iopscience.iop.org/article/10.1088/1742-6596/1640/1/012009) and Makarenko et al, subm. to MNRAS 2023
