# Warnings, Errors and Troubleshooting (WET) list

1. **The *PRE Analysis* flag is set to *True* but other flags upon which it fully or partially depends are set to *False*.**
   a. *PRE Analysis* is only performed over the analysis of condition 3 (z axis), if this flag (do_cond3) is set to *False*, *PRE Analysis* won't be performed.
   b. *PRE Analysis* is performed on *Height* and/or *Volume* ratio calculations, at least one of those flags should be set *True*.
   c. *DELTA_PRE Oscilation* maps are only performed on **Comparisons**, *Perform Comparisons* should *True* for this plot to be printed.
   
2. **No analysis is activated.** Farseer performs analysis on three different dimensions (conditions) of the input dataset, nevertheless, those analysis routines need to be activated in the farseer_user_variables file using variables *do_cond1*, *do_cond2* and *do_cond3*. If all those variables are set to *False*, parsed peaklists with *lost* and *unassigned* residues identified will be exported but no calculation or plot representation will be performed

3. **No plots activated.** Farseer allows the user to configure which parameters are calculated and from those, which kind of plots are drawn. When no plots are turned *ON* Farseer will export only the calculated parameters.

4. **Input x values for restraints fitting do not match data points for condition 1.** Farseer allows fitting of the calculated restraints to specific equations, nevertheless, fitting is only allowed along the *condition 1* data points. For fitting to be performed Farseer requires the user to input a list of values that correspond to the experimental values to be used in as x values in the fitting equation. For example, fitting a CSPs evolution to an increasing ligand concentration requires fitting_x_values variable to be a list of the experimentally investigated ligand concentrations. The number of input values has to match the number of peaklist (.csv files) along *condition 1* and if *condition 1* .csv file names can be converted to number values, those have to match the fitting_x_values variable.

5. **Number of input x values for fitting do not match the number of input peaklists.** Farseer allows fitting of the calculated restraints to specific equations, nevertheless, fitting is only allowed along the *condition 1* data points. For fitting to be performed Farseer requires the user to input a list of values that correspond to the experimental values to be used in as x values in the fitting equation. For example, fitting a CSPs evolution to an increasing ligand concentration requires fitting_x_values variable to be a list of the experimentally investigated ligand concentrations. The number of input values has to match the number of peaklist (.csv files) along *condition 1*.

6. **Negative values in fitting.** There are negative values in titration_x_values variable. Is not normal that negative x values are given to perform a fitting along a titration experiment, nevertheless, Farseer performs the fit accordingly. Confirm the negative values are actually desired and not a typ0.

7. **x values given by the user for fitting look good.** This is not an error nor a warning, it's just an alert to the user about the values used in as x coordinates to perform the fitting.
