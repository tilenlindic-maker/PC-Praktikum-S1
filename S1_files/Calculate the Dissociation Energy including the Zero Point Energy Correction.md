## Normal Mode Analysis

```orca
!PBE0 def2-TZVP OPT FREQ
*xyz 0 1
c 0.0 0.0 0.0
o 0.0 0.0 1.1234
*
```

The new FREQ keyword triggers a normal mode analysis. Search for the vibrational frequency of the molecule in the output (`strg+F` FREQUENCIES)


## **Vibrational Zero Point Energy (ZPE)**

The **Zero Point Energy** is the energy the molecule has at absolute zero (0 K) due to quantum mechanical vibrations. For a diatomic molecule like CO, ZPE can be calculated using the formula:

$\text{ZPE} = \frac{1}{2} h \nu$

where:

- h is Planck's constant ($6.626\times10^{−34}$ Js)
- $\nu$ is the vibrational frequency of the CO molecule in Hz (you might have it in $cm^{-1}$; if so, convert to Hz by multiplying by $c$, the speed of light, $2.998 \times 10^{10} \text{cm/s}$) 
- You furthermore need to convert J into kJ/mol

Then you can add it to the electronic energy and calculate the zero point energy corrected dissociation energy $D_0$. 

![[Calculate Dissociation Energy#Dissociation Energy]]


#### Protocol
- Calculate and compare the dissociation energy ($D_e$) and the zero point energy corrected dissociation energy ($D_0$) . What do you expect of the correction in comparison to the [[CODissoziationEnergyLiterature|literature value]]?



[Calculate the Inner Dissociation Energy](Calculate the Inner Dissociation Energy)
