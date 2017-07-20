*(Don't miss the initial reading about the [Results' folder hierarchy](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/The-results-folder-hierarchy))*

Inside each titration result folder you will find different subfolders that organize the output results data: tables, parsed files and plots.

![Titration folder representation](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/titration_folder.png?raw=true)

The **FullPeaklists/** folder store the parsed peaklist that constitute the titration analysed in *tab separated* files. These peaklists have the same information originally input for the calculation plus additional features:
1. All peaklists are parsed to the same length (number of rows/residues) so that they can be easily compared externally,
2. Identification of *unassigned* and *lost* peaks (Proline residues included),
3. Three additional columns identifying the *residue number*, the *1-letter* aminiacid code, the *3-letter* aminoacid code and a *Peak Status* information.
3. A column for each of the calculated restraint.

The **TablesAndPlots/** subfolder stored the plots drawn. One subfolder is created for each restraint calculated (*H1_delta*, *15N_delta*, *CSP*, *Height_ratio*, ...). Inside each subfolder there is a figure file for each plotting template drawn and a *.tsv* file with the calculated restraints data used for representing those plots. See here the list of [all the plotting templates available](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/Plotting-templates).

The **ChimeraAttributeFiles/** folder stores [Chimera Attribute](https://www.cgl.ucsf.edu/chimera/docs/ContributedSoftware/defineattrib/defineattrib.html) parsed files that can be directly used in [UCSF Chimera](https://www.cgl.ucsf.edu/chimera/) and contain the calculated data for each restraint and each titration data point.
