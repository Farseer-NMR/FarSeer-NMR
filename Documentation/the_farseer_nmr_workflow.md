# Overview of the Farseer-NMR workflow

<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/farseer-workflow.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/farseer-workflow.png?raw=true" width=700></a>

The Farseer-NMR workflow can be summarized in three main steps:
1. Farseer-NMR receives as input two-dimensional NMR peaklists, of several formatting syntaxes,
2. analyses the progression of NMR observables along a titration calculating the derived restraints
3. represents the results in convenient plots and parsed data tables.

# The concept of analysing a titration experiment

Farseer-NMR was thought and is designed to analyse titration NMR experiments. Under these lines, Farseer-NMR receives has input series of peaklists, in the format of *.csv* files, that correspond to a series of experiments in a titration, where there the first peaklist is the reference spectrum to each every other spectra (data points) is going to be compared to. A titration experiment is an experiment setup where the evolution of a system is studied in consequence of the change in a single experimental variable.

<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/titration-scheme.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/titration-scheme.png?raw=true" width=700></a>

# Formatting Peaklits

NMR peaklists derived from titration experiments greatly deviate from ideality: **1)** not every residue in the protein has a peak entry in the peaklists (*unassigned residues*) and **2)** peaks are lost along the titration experiment which results in peaklists files with different sizes, i.e. number of entries or rows. This difference in size greatly difficult the possibility to directly compare the peaklists files in traditional plotting tools, because rows identity won't match when comparing row by row. The first task of Farseer-NMR is to arrange all the input peaklists to the same size by adding *dummy* rows to represent the *unassigned* and *lost* peaks and finally sorting them.

<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/peaklist_completion.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/peaklist_completion.png?raw=true" width=600></a>

## Identifying the *unassigned* and *lost* residues

The first task Farseer-NMR performs is to expand all the peaklists to the same size by adding *dummy* rows corresponding to the *lost* and *unassigned* residues. To achieve this, Farseer-NMR initially creates 4 new columns on the peaklists loaded data tables with the information corresponding to the *residue number*, *1-letter* aminoacid code, *3-letter* aminoacid code and a *Peak Status* column which states whether the peak was *measured*, *lost* or *unassigned*.

<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/peaklist_adding_columns.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/peaklist_adding_columns.png?raw=true" width=400></a>

Afterwards, *lost* residues are identified by comparing a peaklist with the reference one, while *unassigned* residues are (optionally) identified by comparing all the peaklists to a [.fasta file]().

<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/add_lost.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/add_lost.png?raw=true" width=600></a>

<a href="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/add_unassigned.png"><img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/add_unassigned.png?raw=true" width=400></a>

# Performing the Calculations

As described in [analysing a titration experiment](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/The-Farseer-NMR-Workflow#the-concept-of-analysing-a-titration-experiment), Farseer-NMR compares each data point (peaklist) to the reference experiment and calculates the user-required restraints. The results are added as columns in the parsed peaklists, which are exported at the end of the calculation altogether. Farseer-NMR can calculate:

*follow the links for further explanation*
1. Chemical shift perturbations (CSP) for each nuclei
2. [Combined Chemical shift perturbations]()
3. [Data Fitting]()
3. Intensity rations
4. [&#916;PRE](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/The-Delta-PRE-case)

# Plotting the results

Farseer-NMR contains a set of publication-quality plotting templates to represent the calculated data. For each titration analysed, the calculated restraints can be plot in any and every template available. Each template is highly customizable and aims at adapting the data representation to the different publication requimerements. Read further on [how are Farseer-NMR results organized](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/Reading-the-results) and about the [plotting templates available](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/Plotting-templates).


