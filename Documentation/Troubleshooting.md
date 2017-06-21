# Warnings, Errors and Troubleshooting (WET) list

1. The *PRE Analysis* flag is set to *True* but other flags upon which it fully or partially depends are set to *False*.
   a. *PRE Analysis* is only performed over the analysis of condition 3 (z axis), if this flag (do_cond3) is set to *False*, *PRE Analysis* won't be performed.
   b. *PRE Analysis* is performed on *Height* and/or *Volume* ratio calculations, at least one of those flags should be set *True*.
   c. *DELTA_PRE Oscilation* maps are only performed on **Comparisons**, *Perform Comparisons* should *True* for this plot to be printed.
2. 
