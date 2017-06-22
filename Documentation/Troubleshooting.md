# Warnings, Errors and Troubleshooting (WET) list

1. The *PRE Analysis* flag is set to *True* but other flags upon which it fully or partially depends are set to *False*.
   a. *PRE Analysis* is only performed over the analysis of condition 3 (z axis), if this flag (do_cond3) is set to *False*, *PRE Analysis* won't be performed.
   b. *PRE Analysis* is performed on *Height* and/or *Volume* ratio calculations, at least one of those flags should be set *True*.
   c. *DELTA_PRE Oscilation* maps are only performed on **Comparisons**, *Perform Comparisons* should *True* for this plot to be printed.
2. No analysis is activated. Farseer performed analysis on three different dimensions (conditions) of the input dataset, although those analysis routines need to be activated in the farseer_user_variables file using variables *do_cond1*, *do_cond2* and *do_cond3*. If all those variables are set to *False*, parsed peaklists with *lost* and *unassigned* residues identified will be exported and no calculation will be performed
3. Farseer allows the user to configure which parameters are calculated and from those, which kind of plots are drawn. When no plots are turned on Farseer will export only the calculated parameters.
