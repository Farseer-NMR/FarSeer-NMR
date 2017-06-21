CORRECTED:
- 21.06.2017 Remove apply_PRE_smooth flag. All the PRE Analysis is performed when fsuv.apply_PRE_analysis is True.
- 21.06.2017 PRE Analysis now converge all to the same folder: 'PRE_Analysis' inside 'TablesAndPlots'.
- 21.06.2017 removed Titration.writetable() call from farseermain. Now call occurs in Titration.plot_base()
- 21.06.2017 add function Tritration.clean_subplots(), removes/hides subplots not used in the plotting figures.
- 21.06.2017 compacted bar plot last tick label now appears.
TODO:
