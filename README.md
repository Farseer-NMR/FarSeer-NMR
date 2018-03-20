_Website currently under strong development_

![FarSeer Banner](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Figures/FS_banner.png?raw=true)

# Welcome to Farseer-NMR

A fully community driven and ever growing suite to analyse datasets of **peaklist files** extracted from multivariable series of biomolecular NMR experiments. 

With Farseer-NMR, you have:

* Automatic analysis of large and multivariable NMR **peaklist files** datasets
* Peaklist parsing and treatment
* Identification of _missing_ and _unassigned_ residues
* Automatic calculation NMR parameters
* Comprehensive organization of the output results
* Automatic publication ready plot generation
* Full traceability via [Markdown](https://en.wikipedia.org/wiki/Markdown) formatted log file.

## Download

Download the stable release [here](https://github.com/joaomcteixeira/FarSeer-NMR/releases).

## Installation

Farseer-NMR runs on [Unix based systems](https://en.wikipedia.org/wiki/Unix). Attempting to run the current version under Windows machines will fail. Farseer-NMR has been built in its entirety using [Python](https://www.python.org/) libraries and we try to keep it up-to-date with the Python community. To install Farseer-NMR firstly:

1. Unpack the [downloaded](https://joaomcteixeira.github.io/FarSeer-NMR/#Download) version.
1. In your Terminal emulator, navigate to the unpacked Farseer-NMR folder.

There are three different ways to install Farseer-NMR according to your system setup:

### Setting up a Miniconda for Farseer-NMR

The easiest way to setup Farseer-NMR is to install a dedicated Miniconda distribution inside the Farseer-NMR main folder. This setup demands extra disk space (approximatelly 3GBs) but ensures that you can run Farseer-NMR indenpendently from your Python installation setup. Do this with the following steps:

1. Give execution permissions to Linux_install_Miniconda.sh
```
chmod u+rwx Linux_install_Miniconda.sh
```
2. Run Linux_install_Miniconda.sh. This will install a Miniconda distribution with all libraries required to run Farseer-NMR.
```
./Linux_install_Miniconda.sh
```

### With Anaconda already installed

If you use [Anaconda](https://www.anaconda.com/download/) as your Python distribution you can try to run Farseer-NMR directly, most likely all the required libraries are already installed. Alternatively, if you do not want to perturb you main Anaconda Python environment, you can create a secondary [Anaconda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html):

1. Give execution permissions to Linux_install_env.sh
```
chmod u+x Linux_install_env.sh
```
2. Run Linux_install_env.sh. This will create an Anaconda environment with all the required libraries to run Farseer-NMR.
```
./Linux_install_env.sh
```

### Manual installation without Anaconda

If you are an advanced user who is used to manually manage your installed Python libraries, you can get a list of the libraries required to run Farseer-NMR in the corresponding `spec-files` under the Documention folder. Afterwards, to create the run_farseer.sh file run:

```
./Linux_install_manual.sh
```

## Running Farseer-NMR

Before running Farseer-NMR, please read carefully the [Installation](https://joaomcteixeira.github.io/FarSeer-NMR/#installation) section.

1. To run Farseer-NMR:
```
./run_farseer.sh
```

### Running without the GUI

A Farseer-NMR calculation can be run directly from a previously setup folder and from a previously configured `config` file. we advise that only advanced users use this feature and, even for those users, we see no advantage in not using the GUI version because all released features can be configured using the GUI. Only under development features are kept solely in the Core version, these can be accessed (if available) by manually edit of the JSON config file.

```
python <path_to>/farseemain.py <CALCULATION_FOLDER> <CONFIG.JSON>
```

where ```CALCULATION_FOLDER``` is the folder containing the hierarchical ```spectra/``` folder (see Documentation Manual). Whereas the GUI will create the ```spectra/``` folder for you automatically, to run Farseer-NMR from the Core you have to create this folder yourself or use a previously created one, containing the ```peaklists.csv``` files and also FASTA files or of any other necessary files.

The ```CONFIG.JSON``` is any config file saved by the GUI, having or not information on the peaklist experimental tree. It is possible to change the calculation settings manually by editing the ```.json``` configuration file or loading your configuration via GUI and set it up there, you can also take as initial template the ```defaulf_config.json``` provided in the repository.

## Documentation

We have a [Documentation folder](https://github.com/joaomcteixeira/FarSeer-NMR/tree/master/Documentation) where you can find a whole heap of helpful files. There is also an online [Wiki](https://github.com/joaomcteixeira/FarSeer-NMR/wiki) page with additional links and infomation regarding the Farseer-NMR Documentation. These pages are dynamic updated according to the needs of the project/community.

## Tutorials and Examples

Currently we provide a Tutorial folder with artificial datasets that you can use to try out Farseer-NMR and understand its functionalities. We will keep this folder updated as the projects evolves and the interaction with the users also grows. Find our tutorials [here](https://github.com/joaomcteixeira/FarSeer-NMR/tree/master/Documentation/Tutorial_Datasets).

## Participate in the Farseer-NMR community

There are several ways that you can help us improve Farseer-NMR and be part of its community! :-)  

### Reporting a bug

If you find bugs, mis-functional or non-functional features during your calculation runs, please report them by using the [Issues tab](https://github.com/joaomcteixeira/FarSeer-NMR/issues). We have prepared a set of labels that help you to specify the nature of the issues. You can use the tab [Issues tab](https://github.com/joaomcteixeira/FarSeer-NMR/issues) to suggest new features that you would like us to implement or that you would like help implementing.

### Become a collaborator

Help us implement new features! Do you have your own NMR analysis routines that you would like to see implemented in Farseer-NMR? You can fork this project to your own GitHub account, write the functionalities and prepare a pull request for us to review and help you out! We have prepared a [Farseer coding style guide](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Code_Style_Guide_for_Developers.md) for developers so that we keep code readability consistent. We kindly request that contributors to the project adhere to this style guide.

Even if you're not an experienced programmer, please get contact with us and we will be happy join forces with you to introduce your functionalities!

### Mailing list

Post on our [mailing list](https://groups.google.com/forum/#!forum/farseer-nmr) for questions, discussion and help!

## Social Network

Find us on [Research Gate](https://www.researchgate.net/project/Farseer-NMR-automatic-treatment-and-plotting-of-large-scale-NMR-titration-data) and on [Twitter](https://twitter.com/farseer_nmr)!

## License

The entire Farseer-NMR code base comes with no liability and is licensed under the [GPL-3.0](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/COPYING).

<a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/GPLv3_Logo.svg/1200px-GPLv3_Logo.svg.png" width="75" height="37"></a>
