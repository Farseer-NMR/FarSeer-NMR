### The daily problem
Current Biomolecular [NMR][13]-related projects require thoroughly investigation of the system in cause, which usually translates into testing the system against multiple experimental conditions (eg. ligand concentration, ligand nature, temperature, pH, paramagnetic agents, etc...) ultimately generating large datasets that are complex and overload human capability of analysis. Treating datasets of this nature in a fast and straightforward manner is a growing requirement for researchers.
### The solution
Farseer-NMR is a software package that automatically treats, remediates, calculates and plots NMR data and restraints derived from sequencial experiments which measured the response of a system to a single or multiple correlated variables. The process of handling large amounts of diverse NMR data can be tedious, repetitive, error prone and time-consuming; taking days and even weeks in some cases. Farseer-NMR removes the tedium, minimises the effect of human error and reduces the time burden to seconds/minutes.
### How?
Farseer-NMR uses higher-dimensional [Python 3][1] [Numpy][2]/[Pandas][3] arrays to deconvolute complex NMR data into simpler parts which are straightforwardly analysed and represented in a human-readable manner and without information loss. 
### What else?
![coffe][14]
We have implemented the most common (and some not so common) calculation routines (PRE, PCS, CSP, ...) and several **publication-quality** plotting templates to improve data representation. Farseer-NMR is written completely in Python and can read the most common NMR peaklist formats: [Ansig][4], [NmrDraw][5], [NmrView][6], [CYANA][7], [XEASY][8], [Sparky][9] and [CcpNmr Analysis 2.4][10] via simple drag-and-drop import. The graphical interface is written using the most up-to-date version of [PyQt][11], [PyQt v5.8][12], and its modular code base enables facile extension.

[1]:https://www.python.org/
[2]:http://www.numpy.org/
[3]:http://pandas.pydata.org/
[4]:http://rmni.iqfr.csic.es/HTML-manuals/ansig-manual/ansig.html
[5]:https://www.ibbr.umd.edu/nmrpipe/install.html
[6]:http://www.onemoonscientific.com/
[7]:http://www.cyana.org/wiki/index.php/Main_Page
[8]:http://www.bpc.uni-frankfurt.de/guentert/wiki/index.php/XEASY
[9]:https://www.cgl.ucsf.edu/home/sparky/
[10]:http://www.ccpn.ac.uk/v2-software/software/analysis
[11]:https://wiki.python.org/moin/PyQt
[12]:https://pypi.python.org/pypi/PyQt5/5.8
[13]:https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance
[14]:https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/images/Cup-o-coffee-simple.png?raw=true
