# The plots

Farseer-NMR contains a set of plotting templates that represent the calculated data in an organized, simple and **publication-ready** manner. There plots that represent commonly used styles and other which we have specially implemented and developed to improve data representation.

Each generated figure represents the restraint evolution along the whole titration, either in different subplots or concatenated in a single plot.

The structure of the figures, subplots organization in columns and rows, colors, font types and several other plotting style options are highly customizable under the corresponding GUI menu or the farseer_user_variables.py file.

Bellow is represented a dummy example where a randomly generated protein of 100 residues is probed against different concentrations of a ligand (1:0, 1:0.125, 1:0.250, 1:0.5, 1:1, 1:2, 1:4 ratios) which provoke chemical shift perturbations in a specific region.

## Bar Plots

Bar plots represent the evolution of the calculated restraint in configurable and commonly used bar plots. There are three bar plots templates available:  *compacted*, *extended* and *vertical*. 

#### General features
* all text is customizable (font type, size and style)
* X and Y ticks and scales are customizable
* customizable colours for identification of *lost*, *unassigned* and *measured* bars
  * *lost* residues can be represented in three different types ('full', 'prev' or 'zero')
    * 'full', represents full bar
    * 'prev', represents the value of the previously measured point
    * 'zero', represents no value
* customizable bar width
* identification of Proline residues (boolean flag)
* user defined labelling of bars
* user defined colouring of bars
* grid option
* significance threshold line

### Compacted Bar Plot
The compacted bar plots are designed to fit half-page width in a scientific reviewed publication and are generally drawn in an overall figure of cols*rows matrix of subplots.
#### Specific features
* summarized x axis ticks.
* shadowed regions to represent *unassigned* residues.

Compacted Bar Plot | Full Picture in a 3x3 subplot table
------------ | -------------
<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_compacted_1.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_compacted_1.png?raw=true" alt="My picture" width="250"></a> | <a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_compacted.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_compacted.png?raw=true" alt="My picture" width="500"></a>

### Extended Bar Plot
The extended bay plot is designed to fit whole page width in a scientific reviewed publication and are generally drawn in an overall figures vertically stacked subplots representing the titration evolution.
#### Specific features
* bars individually identified by residue labels up to 100 labels (larger proteins get progressively summarized ticks)
* customizable x ticks colours

Extended Bar Plot | Full Picture of vertically stacked subplots
------------ | -------------
<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_extended_1.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_extended_1.png?raw=true" alt="My picture" width="250"></a> | <a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_extended.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_extended.png?raw=true" alt="My picture" height="500"></a>

### Vertical Bar Plots
The vertical bar plot is designed to fit narrow spaces and column organization styles in a scientific reviewed publication and are generally drawn in an overall figures of horizontally stacked subplots representing the titration evolution.

Vertical Bar Plot | Full Picture of horizontally stacked subplots
------------ | -------------
<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_vertical_1.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_vertical_1.png?raw=true" alt="My picture" height="500"></a> | <a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_vertical.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_bar_vertical.png?raw=true" alt="My picture" height="500"></a>

## Residue Evolution Plots
Residue evolution plots represent the evolution of a given restraint over the whole titration for each individual residue. The generated figure is amasses one subplot for each residue in a *mxn* matrix. It is designed to fit a page width under the *Supporting Information* of a scientific manuscript. Individual plots can be cropped externally and used in specific figures of the main article body. The data represented this manner can be fit to a given equation.

#### General features
* Allows data fitting!
* all text and labels are customizable (font type, size and style)
* X and Y ticks and scales are customizable
* customizable colours:
  * shades
  * plot colour
  * fit colour
* customizable lines width
* identification of unassigned and 'lost' residues
  * 'lost' residues have no data point in plots

Residue Evolution Plot | Full Picture representing the whole protein
------------ | -------------
<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_res_evo_1.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_res_evo_1.png?raw=true" alt="My picture" height="250"></a> | <a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_res_evo.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/CSP_res_evo.png?raw=true" alt="My picture" height="500"></a>

## Chemical Shift Scatter Plot
One of the most innovative plots of Farseer-NMR is the Chemical Shift Scatter plot: it translates to a plot the chemical shift evolution in the two observed dimensions (general 1H and 15N) for every residue separately. The generated figure is amasses one subplot for each residue in a *mxn* matrix. It is designed to fit a page width under the *Supporting Information* of a scientific manuscript. Individual plots can be cropped externally and used in specific figures of the main article body.

### General features
* all text and labels are customizable (font type, size and style)
* customizable colours:
  * colour of gradients
  * colour of shapes
  * colour of missing data points ('lost' residues')
* customizable points styles: list of ordered shapes or colour gradient circle.
* identification of unassigned and 'lost' residues
* external configurable rule (default to 0.01 ppm) that is centred at the origin

CSPs Scatter Plot | Full Picture representing the whole protein
------------ | -------------
<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/15N_vs_1H_cs_scatter_1.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/15N_vs_1H_cs_scatter_1.png?raw=true" alt="CSP Scatter Subplot" height="250"></a> | <a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/15N_vs_1H_cs_scatter.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/15N_vs_1H_cs_scatter.png?raw=true" alt="CSP Scatter Plot" height="500"></a>

## Chemical Shift Scatter Flower Plot
Following the idea of the Chemical Shift Scatter Plot, the *Flower* plot amasses all that information on a single plot. The spreading of the chemical shifts away from the centre resemble a flower petals, allowing to easily discriminate those affected residues and to group them according to their changing nature.

<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/15N_vs_1H_cs_scatter_flower.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/15N_vs_1H_cs_scatter_flower.png?raw=true" alt="CSP Scatter Subplot" height="400"></a>
