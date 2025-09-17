# Unsteady Airfoil Dynamics

We adopt Theodorsen's function to model the lift and moment response of an oscillating flat plate and specialise it to the NACA 0012 section used in the AGARD benchmark. The reduced frequency \(k = \omega c / (2 U_\infty)\) is 0.0814 and the complex lift coefficient follows

\[
C_L = 2 \pi \left[ C(k)\left(\alpha + \frac{h}{c}\right) + \frac{1}{2} \alpha \right]
\]

where \(C(k)\) denotes Theodorsen's function, \(\alpha\) the pitch angle, and \(h\) the plunge displacement. We validate the numerical implementation by evaluating the Bessel-function series for \(C(k)\) and confirming the lift phase lag reported by McCroskey (1981). Additional details, including modal coupling coefficients, appear in `notebooks/naca0012_agard.ipynb`.
