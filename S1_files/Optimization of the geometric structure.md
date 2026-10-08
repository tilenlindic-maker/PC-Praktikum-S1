Optimizing the geometric structure of a molecule is a non-trivial high dimensional problem. However, clever algorithms like Newton-Raphson have been developed to deal with these problems. They typically use the first and second derivative - the gradient (dE/dR) and the Hessian matrix. They correspond to the change of energy when changing the atomic coordinates. Let's try to optimize the CO molecule with the internal algorithms of ORCA by adding the keyword **OPT** to the input file.
```orca
!PBE0 def2-TZVP OPT
*xyz 0 1
c 0.0 0.0 0.0
o 0.0 0.0 1.1030
*
```

- Is the structure optimization converged? (The output contains the keyword **HURRAY**, use `Strg+F` in *gedit* to search)
- Document the optimized bond length
- Document the number of cycles

#### Protocol (Optimization of the geometric structure)
- How many cycles did ORCA need (not SCF cycles but geometric optimization steps)?
- How does the program use the gradient and the second derivative to make the process of optimization faster?
- How does the optimized bond distance compare to the experimental value of [1.128 A](https://cccbdb.nist.gov/exp2x.asp?casno=630080&charge=0)

#### Continue with 
[Preparing the Data Set for S2](Preparing the Data Set for S2)
