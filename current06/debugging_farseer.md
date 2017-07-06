# CORRECTED:
## 06.07.2017
- Added WET #9 in FarseerSet.load_experiments().


## 05.07.2017
- Added WET #8 on FarseerSet.load_experiments().
- corrected and improved WET related to fitting.
- WET #5 does not allow negative values.

## 04.07.2017
- Added WET #4.
- Created fslibs/wet.py to store all the WET messages
- farseermain.py -> transferred if-clauses of perform_fits in eval_titrations() to perform_fits().
- Added WET #5, #6, #7, regarding titration_x_values variable and usage.
- added general_variables dictionary in farseermain.init_params() to control lonely vars.

## 22.06.2017
- Added WET #3.

## 21.06.2017
- Added WET #2. In case user sets cond1-3 to False and no calculations are performed.
  - added function FarseerSet.exports_parsed_pkls() and function call on farseermain.gen_titration_dicts().
- added WET on Documentation/
  - Added WET #1 regarding PRE Analysis on farseermain.init_params()
- Remove apply_PRE_smooth flag. All the PRE Analysis is performed when fsuv.apply_PRE_analysis is True.
- PRE Analysis now converge all to the same folder: 'PRE_Analysis' inside 'TablesAndPlots'.
- removed Titration.writetable() call from farseermain. Now call occurs in Titration.plot_base()
- added function Tritration.clean_subplots(), removes/hides subplots not used in the plotting figures.
- compacted bar plot last tick label now appears.

TODO:
