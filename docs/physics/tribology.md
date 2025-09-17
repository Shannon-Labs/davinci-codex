# Rolling Tribology Models

Rolling friction encapsulates hysteretic deformation, lubricant shear, and contact micro-slip. The Bowden & Tabor measurements provide the baseline coefficient of friction curve:

\[
\mu = \mu_0 + A \sqrt{V} + B V
\]

where \(V\) is surface speed and \(A\), \(B\) incorporate lubricant viscosity and surface temperature feedback. The Chrono discrete-element model integrates a Greenwood-Williamson asperity ensemble and Vogel-Fulcher lubricant rheology, producing speed-dependent friction trends that we compare directly in `notebooks/rolling_friction_validation.ipynb`.
