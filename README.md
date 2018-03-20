![FarSeer Banner](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Figures/FS_banner.png?raw=true)

Find, download and fork the full project at [GitHub](https://github.com/joaomcteixeira/FarSeer-NMR).

_Website currently under development_

# Welcome to Farseer-NMR

A fully community driven and ever growing suite to analyse **peaklist files** extracted from multivariable series of biomolecular NMR experiments. Up to three different experimental variables can be combined and analysed together.  
With Farseer-NMR, you can automatically calculate structural parameters from peaklist datasets, which are then comprehensively and conveniently represented in publication-ready plots.

Conveniently save and load your configuration files and re-run your operations with one-click!

Full traceability via [Markdown](https://en.wikipedia.org/wiki/Markdown) formatted log file.

## Download

Download the stable release [here](https://github.com/joaomcteixeira/FarSeer-NMR/releases).

## Installation

Farseer-NMR runs on [Unix based systems](https://en.wikipedia.org/wiki/Unix). Attempting to run the current version under Windows machines will fail. Farseer-NMR has been built in its entirety using [Python](https://www.python.org/) libraries and we try to keep it up-to-date with the Python community. Bellow, three different ways to install Farseer-NMR.

### Setting up a Miniconda for Farseer-NMR

The easiest way to setup Farseer-NMR is to install a separated Miniconda distribution inside the Farseer-NMR main folder. This setup demands extra disk space (approximatelly 3GBs) but ensures that you can run Farseer-NMR indenpendently from you Python installation setup. Do this with the following steps:

1. Unpack the downloaded version.
1. Navigate to the Farseer-NMR folder.
1. Give execution permissions to Linux_install.sh
```
chmod u+rwx Linux_install.sh
```
1. Inside the Farseer-NMR folder run Linux_install.sh, this will install a Miniconda distribution with everythin necessary to run Farseer-NMR.
```
./Linux_install.sh
```

### With Anaconda already installed

If you use [Anaconda](https://www.anaconda.com/download/) as your Python distribution you can try to run Farseer-NMR directly, most likely all the required libraries are already installed. Otherwise, is you do not want to perturb you main Anaconda Python environment, you can create a secondary [Anaconda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html) for Farseer-NMR using the corresponding `spec-files` under the Documention folder. For example for 64-bit machines:

```
conda create --name farseernmr --file spec-file_64bit.txt
```

Give execution persions to the running script:
```
chmod u+x run_farseer.sh
```

### Manual installation without Anaconda

If you are an advanced user who is used to manually manage your installed Python libraries, you can get a list of the libraries required to run Farseer-NMR in the corresponding `spec-files` under the Documention folder.

## Running Farseer-NMR

Before running Farseer-NMR, please read carefully the [Installation](https://joaomcteixeira.github.io/FarSeer-NMR/#installation) section.

There are two ways to run Farseer-NMR: using the fully featured graphical user interface (GUI) or directly in a ```Terminal``` emulator. There are no advantages to running Farseer-NMR directly on the command line, rather than using the GUI version. All released features can be configured using the GUI; only under development features are kept solely in the Core (terminal version) and can be accessed (if available) by direct editing the JSON config file.

We **strongly** advise users to run the GUI version.  

### Using the GUI

1. Run Farseer-NMR GUI version:
```
./run_farseer.sh
```

### Running without the GUI

_If you reading this section we assume you are an advanced user, so we skip any further instructions._

```
python <path_to>/farseemain.py <CALCULATION_FOLDER> <CONFIG.JSON>
```

where ```CALCULATION_FOLDER``` is the folder containing the hierarchical ```spectra/``` folder. The GUI will create the ```spectra/``` folder for you automatically, whereas to run Farseer-NMR via the terminal you have to create it yourself or use a previously created one, this includes ```peaklists.csv``` files and also FASTA files or of any other kind necessary for the calculation to run.

## Advanced considerations on the CONFIG file

The ```CONFIG.JSON``` is any config file saved by the GUI, having or not information on the peaklist experimental tree. It is possible to change the calculation settings manually by editing the ```.json``` configuration file or loading your configuration via GUI and set it up there, you can also take as initial template the ```defaulf_config.json``` provided in the repository. But consider, unless you are developing new features, we don't see a point in doing this rather than using the GUI. :-P

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

The entire Farseer-NMR code base comes with no liability and is licensed under the GPL-3.0.

<a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/GPLv3_Logo.svg/1200px-GPLv3_Logo.svg.png" width="75" height="37"></a>
