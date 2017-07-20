**The Backbone/ and Sidechains/ folders** are created in the main calculation folder and separate the results obtained for backbone atoms and for side-chains atoms (if present). Farseer-NMR separates these two types of results because, by experience, concatenating results for backbone atoms and side-chains atoms inside the same tables and plots results in awkward representations.

**The *Calculations/* folder:** appears under *Backbone/* or *Sidechains/* folders and store data generated for the different titration sets analysed along each condition.

**The conditions subfolders** store the results of the different sets of the analysed titrations and are numbered accordingly to the condition variable that defines the set (*cond1/*, *cond2/* and *cond3/*) - see also [Farseer Cube](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/The-Farseer-NMR-Cube). The *cond\**/ folder tree respects the hierarchy of the *spectra/* folder where each subfolder is a titration of the *cond\**/ set. **Example:** the results generated for a titration performed at *298K* for ligand *L1*, will be stored under the following folder tree: *Backbone/Calculations/cond1/298/L1/*. Each of these titration subfolders store the corresponding **Farseer-NMR generated files**.

![Example of a Farseer-NMR calculation folder](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/results_hierarchy.png?raw=true)

Continue [reading the titration results](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/Reading-the-results)...
