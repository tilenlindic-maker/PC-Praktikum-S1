### Inner Energy \( $U$ \) for CO

At room temperature, we need to account for the mechanical energy of a molecule.
First, we separate the problem of the mechanical energy of a molecule, by separating it into contributions from translation $U_{\text{trans}}$  , rotation $U_{\text{rot}}$ and vibration $U_{\text{vib}}$.
$$
U_{\text{CO}} = E_{\text{el}} + E_{\text{zpe}} + U_{\text{trans}} + U_{\text{rot}} + U_{\text{vib}}
$$
Expressions for these contributions exist for ideal gases and we will apply the following formulas:

#### 1. **Translational Internal Energy $U_{\text{trans}}$:**
$$
U_{\text{trans}} = \frac{3}{2} k_B T
$$
This result comes from the translational energy in three dimensions for an ideal gas.

#### 2. **Rotational Internal Energy $U_{\text{rot}}$:**
For a diatomic molecule like CO, the rotational internal energy at high temperatures is:

$$
U_{\text{rot}} = k_B T
$$

#### 3. **Vibrational Internal Energy $U_{\text{vib}}$:**
The vibrational contribution to internal energy is

$$
U_{\text{vib}} = \frac{h \nu}{e^{\frac{h \nu}{k_B T}} - 1}
$$

where the second term is the temperature correction factor, accounting for vibrational excitation at non-zero temperatures.

So, the **final internal energy** $U_{\text{CO}}$ can be written as:

$$
U_{\text{CO}} = \frac{3}{2} k_B T + k_B T + \frac{h \nu}{e^{\frac{h \nu}{k_B T}} - 1} 
$$

For atoms, we only need to consider the translational contributions to the inner energy.
   $$
   U_{\text{atom}} = E_{\text{el, atom}} + \frac{3}{2} k_B T
   $$

#### Protocol (Inner Energy)
Using the formulas above, calculate the inner dissociation energy of CO 
$$
\Delta U = U_{\text{C}} + U_{\text{O}} - U_{\text{CO}}.
$$

Now, we can account for the mechanical energy of a molecule at room temperature.
Compare the calculated value to the [[CODissoziationEnergyLiterature|literature value]] and discuss the quality of the correction.


#### Back to
[S1 Quantum Chemistry on the Computer](S1 Quantum Chemistry on the Computer)
