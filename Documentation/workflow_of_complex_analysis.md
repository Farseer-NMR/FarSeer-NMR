# The concept of multi-variable experimental setups
To investigate the complex dependency of a system on multiple variables one typically records a series of experiments in which one of the variables is systematically varied while the others are kept as fixed parameters. Progressive change of the parameters generates an array of experiments that obey a multivariable logic.  

### Consider the following example:
> Given a protein system **P**, the binding profile of the ligand **L1** was measured at five concentrations (**C**) and at temperature **T1**. The same protein **P** was screened against four related ligands (**L1**, **L2**, **L3**, **L4**) and each experiment was repeated at three different temperatures (**T1**, **T2**, **T3**). This setup embodies a set of 12 experimental series which result from the combination of two continuous conditions (temperature and concentration) and one discontinuous variable (ligand nature). In total, 60 2D-NMR experiments were acquired (5\*4\*3). Potentially, this dataset contains information on the ligand binding site, affinity of binding and their dependency with temperature. NMR data are sensitive to the contribution of each experimental variable. In order to fully understand the system under study is essential to have a flexible, yet simple, way to access the data that preserves the complete information and allows the deconvolution of those complex contributions.

Farseer-NMR exploits the power of Numpy and Pandas Python libraries to analyse the dependency of NMR parameters to multiple variables simultaneously (eg. ligand concentration, ligand nature, temperature, pH, paramagnetic agents, etc...). Thus, the exquisite (but complex) sensitivity of NMR parameters to nuclear environment can be exploited and interpreted fully with minor effort from the user.

## Organizing datasets into multidimensional arrays
To freely navigate and explore experimental datasets spanning multiple conditions, Farseer-NMR loads the whole input data to a single digital object, a Python [Numpy](http://www.numpy.org/)/[Pandas](http://pandas.pydata.org/) **five-dimensional array**; which, for the sake of simplicity, can be visualized as a cube made of 2D data points, where the three-dimensional axes of the cube (x, y, z) are the experimental variables, in our example, ligand concentration, ligand nature and temperature range, and each data point is a 2D-NMR peaklist with the respective rows (residues) and columns (experimental observables) extracted from the user preferred NMR analysis suite. We have called this object the **Farseer-NMR Cube**.

![preparation of the farseer-NMR cube](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/preparation_of_cube.jpg?raw=true)

## Reading the data

The great advantage of having the whole experimental dataset in a single digital object, the Farseer-NMR Cube, is that it can be arbitrarily sliced to investigate specific questions that are not limited to the acquisition schedule of the multivariate data. [Following the above example](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/Workflow-for-complex-analysis/_edit#consider-the-following-example), we can query the dataset to different questions that directly relate to the conditions assayed:

1. *Ligand concentration range:*
   a. Where does the *ligand* bind to the *protein system* **P**?
   b. Are there multiple binding sites or allosteric effects?
   c. What are the *ligand concentration* dependencies of these effects?
   d. What is the binding constant?
  
2. *Ligand Nature:*
   a. What is the binding profile of the various *ligands*?
   b. Do the ligands interact with the same binding site? 
   c. Do they provoke the same changes in **P**?

3. *Temperature variations:*
   a. How does the *temperature* affects the binding profiles of the ligand library?

As explained above, the the Farseer-NMR Cube's three-dimensional axes correspond to the progression along the three experimental assayed conditions and, therefore, we can explore the above cited questions by slicing the cube along the different axes, where **1**, **2** and **3** correspond to **x**, **y** and **z**, respectively. Further developing this procedure, we can fix two points in two given axes (say x=**C2** and z=**T2**) and slice along the third axis (y) to generate single 1D-vectors of 2D-NMR peaklists. These vectors are, indeed, independent series of experiments that are defined by the variation of a condition with the other 2 variables fixed at a value/condition. In this way, out of the 12 experimentally acquired series that relate to the ligand concentration (4\*3, in our example), *Farseer-NMR can extract up to 47* in silico *generated experimental series* that result from the different combinations of the experimental variables:

* 4\*3 (ligand concentration)
* 3\*5 (ligand nature)
* 5\*4 (temperature dependence)

For each experimental set extracted, Farseer-NMR executes the [whole analysis workflow](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/The-Farseer-NMR-Workflow), where restraints are calculated and data are plotted.

<img src="https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/cube_workflow.gif?raw=true" width=400>
