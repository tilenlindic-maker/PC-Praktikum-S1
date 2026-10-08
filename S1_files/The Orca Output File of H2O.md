(Source: https://www.orcasoftware.de/tutorials_orca/first_steps/input_output.html)

The first part of the output is a header with references to contributors and basis set information. After that come the WARNINGS, that should be carefully checked and:
```orca
****************************
* Single Point Calculation *
****************************
```

as a reference to the kind of calculation that will be performed. Then comes detailed information about the integral module (SHARK) and SCF parameters:
```orca
----------------------
SHARK INTEGRAL PACKAGE
----------------------

Number of atoms                             ...      2
Number of basis functions                   ...     19
Number of shells                            ...      9
Maximum angular momentum                    ...      2
Integral batch strategy                     ... SHARK/LIBINT Hybrid
RI-J (if used) integral strategy            ... SPLIT-RIJ (Revised 2003 algorithm where possible)
Printlevel                                  ...      1
Contraction scheme used                     ... SEGMENTED contraction

[...]

------------
SCF SETTINGS
------------
Hamiltonian:
 Ab initio Hamiltonian  Method          .... Hartree-Fock(GTOs)
 RI-approximation to the Coulomb term is turned on
   Number of auxiliary basis functions  .... 371
   RIJ-COSX (HFX calculated with COS-X)).... on

General Settings:
 Integral files         IntName         .... teste
 Hartree-Fock type      HFTyp           .... RHF
 Total Charge           Charge          ....    0
 Multiplicity           Mult            ....    1

[...]
```

Then the initial guess is built:
```
------------------------------
INITIAL GUESS: MODEL POTENTIAL
------------------------------
Loading Hartree-Fock densities                     ... done
Calculating cut-offs                               ... done
Setting up the integral package                    ... done
Initializing the effective Hamiltonian             ... done
Starting the Coulomb interaction                   ... done (   0.0 sec)
Reading the grid                                   ... done
Mapping shells                                     ... done
Starting the XC term evaluation                    ... done (   0.0 sec)
Transforming the Hamiltonian                       ... done (   0.0 sec)
Diagonalizing the Hamiltonian                      ... done (   0.0 sec)
Back transforming the eigenvectors                 ... done (   0.0 sec)
Now organizing SCF variables                       ... done
```

and if the SCF converges, you will see a message, together with a discrimination of the energy components:
```orca
            *****************************************************
            *                     SUCCESS                       *
            *           SCF CONVERGED AFTER   8 CYCLES          *
            *****************************************************

----------------
TOTAL SCF ENERGY
----------------

Total Energy       :          -75.95933513 Eh           -2066.95859 eV

Components:
Nuclear Repulsion  :            9.06276654 Eh             246.61041 eV
Electronic Energy  :          -85.02210166 Eh           -2313.56901 eV
One Electron Energy:         -122.82422006 Eh           -3342.21694 eV
Two Electron Energy:           37.80211839 Eh            1028.64794 eV

Virial components:
Potential Energy   :         -151.67568240 Eh           -4127.30515 eV
Kinetic Energy     :           75.71634727 Eh            2060.34656 eV
Virial Ratio       :            2.00320919
```

The **orbitals energies** are printed (along with charges and timings): 
```orca
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
```
The final calculated energy is printed as:
```orca
-------------------------   --------------------
FINAL SINGLE POINT ENERGY       -75.324154395464
-------------------------   --------------------
```
after which the dipole moment for the system is printed and the file ends.


[co.out](co.out)
