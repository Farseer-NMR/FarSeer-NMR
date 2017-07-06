# Warnings, Errors and Troubleshooting (WET) list

1. **The *PRE Analysis* flag is set to *True* but other flags upon which it fully or partially depends are set to *False*.**
   a. *PRE Analysis* is only performed over the analysis of condition 3 (z axis), if this flag (do_cond3) is set to *False*, *PRE Analysis* won't be performed.
   b. *PRE Analysis* is performed on *Height* and/or *Volume* ratio calculations, at least one of those flags should be set *True*.
   c. *DELTA_PRE Oscilation* maps are only performed on **Comparisons**, *Perform Comparisons* should *True* for this plot to be printed.
   
2. **No analysis is activated.** Farseer performs analysis on three different dimensions (conditions) of the input dataset, nevertheless, those analysis routines need to be activated in the farseer_user_variables file using variables *do_cond1*, *do_cond2* and *do_cond3*. If all those variables are set to *False*, parsed peaklists with *lost* and *unassigned* residues identified will be exported but no calculation or plot representation will be performed

3. **No plots activated.** Farseer allows the user to configure which parameters are calculated and from those, which kind of plots are drawn. When no plots are turned *ON* Farseer will export only the calculated parameters.

4. **Input x values for restraints fitting do not match data points for condition 1.** Farseer allows fitting of the calculated restraints to specific equations, nevertheless, fitting is only allowed along the *condition 1* data points. For fitting to be performed Farseer requires the user to input a list of values that correspond to the experimental values to be used in as x values in the fitting equation. For example, fitting a CSPs evolution to an increasing ligand concentration requires fitting_x_values variable to be a list of the experimentally investigated ligand concentrations. The number of input values has to match the number of peaklist (.csv files) along *condition 1* and if *condition 1* .csv file names can be converted to number values, those have to match the fitting_x_values variable.

5. **Number of input x values (coordinate axis) do not match the number of input peaklists.** Farseer allows fitting of the calculated restraints to specific equations, nevertheless, fitting is only allowed along the *condition 1* data points. For fitting to be performed Farseer requires the user to input a list of values that correspond to the experimental values to be used in as x values in the fitting equation. For example, fitting a CSPs evolution to an increasing ligand concentration requires *fitting_x_values* variable to be a list of the experimentally investigated ligand concentrations. The number of input values has to match the number of peaklist (.csv files) along *condition 1*, where 0 relates to the reference experiment (peaklist). Even if fitting is disabled, *fitting_x_values* can be used for Residue Evolution Plot if *res_evo_set_x_values* flag, *fitting_x_values* has to match number of peaklists input.

6. **There are negative values in titration_x_values variable.** Farseer has implemented fitting only to the Hill Equation (http://www.physiologyweb.com/calculators/hill_equation_interactive_graph.html) which does not consider the use of negative values in the coordinate axis. Please correct your input data in titration_x_values variable.

7. **x values given by the user for fitting look good.** This is not an error nor a warning, it's just an alert to the user about the values used in as x coordinates to perform the fitting.

8. **Files are missing in the input folder tree.** Farseer assumes that when analysing different titrations together, those are related. Therefore the same number of files (data points) should be given for every condition. For example, there should be the same number of peaklists (.csv files) in each subfolder, as well as the same subfolder tree should be maintained under spectra/.

9. **There are no files of the file type.** You have asked Farseer to read a certain file type that does not exist in the spectra/ folder.
