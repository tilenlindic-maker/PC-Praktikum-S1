## Optimizing the geometric structure of CO


![[Pasted image 20260610140652.png]]

The plot above shows descrete points of the potential energy surface of CO. We would be interested in the minimum of the curve, but we do not have an analytic form of the function. 
To approximate the minimum, we need a numerical approach which has to be executed iteratively. Can you guess an approximate minimum by using the data obtained from your scan? Use this **most important piece of information** in the upcoming task !


#### Goal:
- Optimize the bond length of CO (no more than 3 digits behind the comma)


#### Task description

```orca
!PBE0 def2-TZVP
*xyz 0 1
c 0.0 0.0 0.0
o 0.0 0.0 1.300
*
```

Here is an example input to start. It only executes the calculation of a single CO distance (1.000 Angstrom). We can call this file `co_1.300.inp`, to remember the distance between C and O. 
However, it is only the filename and has no consequences on the calculation itself.



### Algorithm
- `DISTANCE` should refer to the distance in the input file.

- Create a new input with `gedit`.
```
gedit co_DISTANCE.inp
```
- change the bond length of CO in the xyz block of the file to your needs 
- close `gedit` and execute an orca calculation
	`orca co_DISTANCE.inp > co_DISTANCE.out`
- to document the distance energy pairs, first open the calculation output look for FINAL in the output and paste the corresponding number into Libre Office Calc. 
```
gedit co_DISTANCE.out
```

- With your new knowledge, think of the next distance 
	and repeat to minimize the energy, iteratively. Everyone should do this 10 times.
	*Now would be a good time to look at your partners results. It would be important for the practicum S2 to not end up with all of you having the same distance energy pairs*

In the end, everyone should be able to contribute 5-10 energy distance pairs to a data set used for the practicum S2. Ideally, they are spread around the minimum, but **every point counts**. However, without **proper communication** you might end up with all of you having the same data and duplicate distances are of course redundant.

#### Using the Interval Method (optional)

If you finished, get bored or would like to understand a more complicated algorithm, 
there are nice systematic ways of dealing with this problem like [The Interval Method](The Interval Method)


#### Protocol (Geometry Optimization Exercise)

- How did you and your group approach the problem? Summarize crudely. 
- Would you be able to find the minimum of a large molecule with your approach?


#### Continue with:
[[Optimization of the geometric structure|Optimize the geometric structure using internal algorithms of the orca program]]

