
Open the file co.inp and save the output below in the new file.
```sh
gedit co.inp
```

Insert the following content in the white graphical user interface.

![ExampleInput](ExampleInput)

- PBE0: The hybrid density functional of Perdew Burke and Ernzerhof. The corresponding papers are mentioned upon the [most cited papers ever](https://www.nature.com/news/the-top-100-papers-1.16224)
- def2-TZVP: def2 "Karlsruhe" **T**riple **Z**eta **V**alence **P**olarization Basis Set, 
- LARGEPRINT: tells the program to write the eigenvectors of the electronic structure into the output. Why is this necessary for visualizing the molecular orbitals?
- xyz: Cartesian Coordinates
- 0 1: 0 => Charge, 1 => Singlet Multiplicity (What is the multiplicity and how does it relate to the number of unpaired electrons?)
- 1.1: Minimum Distance for Hartree Fock with this basis set in Angstrom


### Run the calculation by:
```
orca co.inp > co.out
```

### Open the orca output file with your text editor:
```sh
gedit co.out
```

### Familiarize with the output

```orca
                                 *****************
                                 * O   R   C   A *
                                 *****************

                                            #,
                                            ###
                                            ####
                                            #####
                                            ######
                                           ########,
                                     ,,################,,,,,
                               ,,#################################,,
                          ,,##########################################,,
                       ,#########################################, ''#####,
                    ,#############################################,,   '####,
                  ,##################################################,,,,####,
                ,###########''''           ''''###############################
              ,#####''   ,,,,##########,,,,          '''####'''          '####
            ,##' ,,,,###########################,,,                        '##
           ' ,,###''''                  '''############,,,
         ,,##''                                '''############,,,,        ,,,,,,###''
      ,#''                                            '''#######################'''
     '                                                          ''''####''''
             ,#######,   #######,   ,#######,      ##
            ,#'     '#,  ##    ##  ,#'     '#,    #''#        ######   ,####,
            ##       ##  ##   ,#'  ##            #'  '#       #        #'  '#
            ##       ##  #######   ##           ,######,      #####,   #    #
            '#,     ,#'  ##    ##  '#,     ,#' ,#      #,         ##   #,  ,#
             '#######'   ##     ##  '#######'  #'      '#     #####' # '####'



                  #######################################################
                  #                        -***-                        #
                  #          Department of theory and spectroscopy      #
                  #    Directorship and core code : Frank Neese         #
                  #        Max Planck Institute fuer Kohlenforschung    #
                  #                Kaiser Wilhelm Platz 1               #
                  #                 D-45470 Muelheim/Ruhr               #
                  #                      Germany                        #
                  #                                                     #
                  #                  All rights reserved                #
                  #                        -***-                        #
                  #######################################################

```


```
--------------
SCF ITERATIONS
--------------
ITER       Energy         Delta-E        Max-DP      RMS-DP      [F,P]     Damp
               ***  Starting incremental Fock matrix formation  ***
                            ****Activating DIIS****
  0   -112.7871522064   0.000000000000 0.00000059  0.00000003  0.0000010 0.0000
                 **** Energy Check signals convergence ****

               *****************************************************
               *                     SUCCESS                       *
               *           SCF CONVERGED AFTER   1 CYCLES          *
               *****************************************************


```

- After how many cycles did *YOUR* calculation converge?

```
----------------
ORBITAL ENERGIES
----------------

  NO   OCC          E(Eh)            E(eV)
   0   2.0000     -20.664029      -562.2968
   1   2.0000     -11.349402      -308.8329
   2   2.0000      -1.539471       -41.8911
   3   2.0000      -0.806502       -21.9460
   4   2.0000      -0.651461       -17.7272
   5   2.0000      -0.651461       -17.7272
   6   2.0000      -0.551476       -15.0064
   7   0.0000       0.136911         3.7255
   8   0.0000       0.136911         3.7255
   9   0.0000       0.213499         5.8096
  10   0.0000       0.286301         7.7907
  11   0.0000       0.356903         9.7118
  12   0.0000       0.356903         9.7118
  13   0.0000       0.497066        13.5259
  14   0.0000       0.646322        17.5873
  15   0.0000       0.646322        17.5873
  16   0.0000       0.811667        22.0866
  17   0.0000       0.817847        22.2548
  18   0.0000       0.817847        22.2548

```

- occupation (OCC): number of electrons occupying the orbital
- Identify any degenerate orbitals. 
- What do you learn from the **ORBITAL ENERGIES** ?


- Note the value of the **FINAL SINGLE POINT ENERGY** of *YOUR* file

```
-------------------------   --------------------
FINAL SINGLE POINT ENERGY      -112.787152206713
-------------------------   --------------------


                            ***************************************
                            *     ORCA property calculations      *
                            ***************************************

                                    ---------------------
                                    Active property flags
                                    ---------------------
   (+) Dipole Moment


------------------------------------------------------------------------------
                       ORCA ELECTRIC PROPERTIES CALCULATION
------------------------------------------------------------------------------

Dipole Moment Calculation                       ... on
Quadrupole Moment Calculation                   ... off
Polarizability Calculation                      ... off
GBWName                                         ... co.gbw
Electron density                                ... co.scfp
The origin for moment calculation is the CENTER OF MASS  = ( 0.000000,  0.000000  1.190568)

-------------
DIPOLE MOMENT
-------------
                                X             Y             Z
Electronic contribution:      0.00000       0.00000      -0.06197
Nuclear contribution   :      0.00000       0.00000       0.00700
                        -----------------------------------------
Total Dipole Moment    :      0.00000       0.00000      -0.05498
                        -----------------------------------------
Magnitude (a.u.)       :      0.05498
Magnitude (Debye)      :      0.13974



--------------------
Rotational spectrum
--------------------

Rotational constants in cm-1:     0.000000     2.019701     2.019701
Rotational constants in MHz :     0.000000 60549.098652 60549.098652

 Dipole components along the rotational axes:
x,y,z [a.u.] :    -0.054976     0.000000     0.000000
x,y,z [Debye]:    -0.139737     0.000000     0.000000



Timings for individual modules:

Sum of individual times         ...        0.855 sec (=   0.014 min)
GTO integral calculation        ...        0.225 sec (=   0.004 min)  26.3 %
SCF iterations                  ...        0.630 sec (=   0.011 min)  73.7 %
                             ****ORCA TERMINATED NORMALLY****
TOTAL RUN TIME: 0 days 0 hours 0 minutes 1 seconds 46 msec

```




#### Protocol (Optimization of Electronic Structure)
- How many SCF Cycles did your calculation need to converge?
- What did you use in this calculation? (Method, Basisset, Program (Version))
- Why is this necessary for visualizing the molecular orbitals?
- What is the multiplicity and how does it relate to the number of unpaired electrons?


#### Continue: 
[AvogadroGuide](AvogadroGuide)

#### Back to:
[S1 Quantum Chemistry on the Computer](S1 Quantum Chemistry on the Computer)
