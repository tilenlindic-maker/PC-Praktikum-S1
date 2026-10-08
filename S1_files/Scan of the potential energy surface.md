#### Surface Scan
A surface scan in quantum chemistry executes several calculations with varying bond length. In this example, we will scan the bond length of the CO molecule to get an overview of its potential energy surface.  Scan the potential energy surface of CO by putting the input below into a new file called "scan.inp".

```
gedit scan.inp
```

```orca
!UKS PBE0 def2-TZVP
%paras
R= 0.8, 6, 25
end
*xyz 0 1
c 0.0 0.0 0.0
o 0.0 0.0 {R}
*
```

Close `gedit` before typing things in the terminal again. Then type 

```
orca scan.inp > scan.out
```
to execute the orca calculation.

- The **R**  is set as a variable in the *paras* block. It corresponds the bond length of CO, which elongates from 0.7 - 10 A in 25 steps. We meet the **R** again in the xyz section.
- You will find the obtained **energy data** on the bottom of the output file. Plot the data **as scatter plot** in libre office calc (Excel).

#### Plotting

![[Pasted image 20260610140652.png]]


#### Caveat

The dissociation of CO is calculated as singlet, but the separated atoms both have triplet states.
Hence, we get a multireference character, and we need to make sure to find the lowest possible state. This is not content of this exercise. However, recognize that the multireference character actually forbids us to simple read the dissociation energy from this plot.

#### Protocol (Scan of the Potential Energy Surface)
- Is this plot the same as a Morse potential?
- Do you see a jump in your PES scan? If so, why?
- How does the dissociation energy compare to the one calculated later, through the direct approach? (Why might it differ?)


#### Continue with
[Geometry Optimization Exercise](Geometry Optimization Exercise)
