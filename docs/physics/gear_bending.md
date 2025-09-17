# Gear Tooth Bending Theory

The Lewis bending equation estimates the root stress of a spur gear tooth modelled as a cantilever:

\[
\sigma = \frac{F_t}{b m} \cdot \frac{6 y}{m}
\]

where \(F_t\) is the transmitted tangential force, \(b\) the face width, \(m\) the module, and \(y\) the form factor. Our finite-element model matches the Lewis form factor of 0.31 for a 32-tooth gear with a 20° pressure angle. The CalculiX simulation solves the quadratic tetrahedral system and extracts the root stress directly, enabling comparison with the analytical prediction and modern material substitutions. Analysts can reproduce the calculation via `notebooks/gear_bending_validation.ipynb`.
