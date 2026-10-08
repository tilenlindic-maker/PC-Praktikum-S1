The interval method is a straightforward **optimization technique** that’s especially useful in cases like finding the optimal bond length of a diatomic molecule. It essentially involves narrowing down the interval within which the minimum (or maximum) distance is located, based on repeated evaluations of the potential energy.

1. **Choose Initial Points**:
    
    - Start with three distance-points $a$, $b$, and $c$ with $a<b<c$. Set these points wide enough to contain the expected minimum of the curve.
	

2. **Calculate Energies**:
    
    - Evaluate the potential energy at points $a$, $b$, and $c$: $f(a)$, $f(b)$, and $f(c)$ with orca.
	
3. **Create Intervals and Midpoints**:
    
    - Define two intervals: $[a,b]$ and $[b,c]$.
    - Calculate the midpoints of each interval: $m_{ab}=\frac{(a+b)}{2}$  and $m_{bc}=\frac{(b+c)}{2}$
    - Calculate the potential energy at $m_{ab}$  and $m_{bc}$ : $f(m_{ab})$ and $f(m_{bc}​$) with orca.
	
4. **Select the Three Lowest Points**:
    
    - Out of the five points $a$, $m_{ab}$, $b$, $m_{bc}$​, and $c$, keep the three points with the lowest energies.
	
5. **Repeat the Process**:
    
    - With the three remaining points, repeat steps 3 and 4. Each iteration refines the search by focusing on the part of the interval that likely contains the minimum.
	
6. **Stopping Criterion**:
    
    - Stop once the interval between the outer points $a$ and $c$ is sufficiently small (up to 0.001 A).

#### Back to:
[Geometry Optimization Exercise](Geometry Optimization Exercise)
