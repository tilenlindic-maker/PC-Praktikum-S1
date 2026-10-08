Use the energy of the molecule with the optimized bond length (1.1234 A) as energy of CO.

#### Atom Calculations
Execute calculations of the atoms with these input files: 

---

```sh
gedit c.inp
```

```orca
!UKS PBE0 def2-TZVP
*xyz 0 3
c 0.0 0.0 0.0
*
```

```
orca c.inp > c.out
```

---

```sh
gedit o.inp
```

```orca
!UKS PBE0 def2-TZVP
*xyz 0 3
o 0.0 0.0 0.0
*
```

```
orca o.inp > o.out
```

---
**CAVEATE** Pay attention to the change in the multiplicity !

## Find Electronic Energies ($E_C$, $E_O$, $E_{CO}$) in the output files
- Look for "FINAL SINGLE POINT ENERGY" in the output-file 

#### Calculate the Dissociation Energy
![[Calculate Dissociation Energy#Dissociation Energy]]


#### Protocol (Dissociation Energy)
- Compare the herein obtained dissociation energy with the dissociation energy of the [[CODissoziationEnergyLiterature|literature value]]. Which of the two literature values do you need to compare to?


#### Continue with
[Calculate the Dissociation Energy including the Zero Point Energy Correction](Calculate the Dissociation Energy including the Zero Point Energy Correction)


