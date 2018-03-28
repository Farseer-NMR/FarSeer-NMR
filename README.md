_Website currently under strong development_

![FarSeer Banner](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Figures/FS_banner.png?raw=true)

# Welcome to Farseer-NMR

A fully community driven and ever growing suite to analyse datasets of **peaklist files** extracted from multivariable series of biomolecular NMR experiments. 

With Farseer-NMR, you have:

* Automatic analysis of large and multivariable NMR **peaklist files** datasets
* Peaklist parsing and treatment
* Identification of _missing_ and _unassigned_ residues
* Automatic calculation of NMR parameters
* Comprehensive organization of the output
* Large suite of publication-ready plotting templates
* Full traceability via [Markdown](https://en.wikipedia.org/wiki/Markdown) formatted log file.

## Project Repository and Download

You can download the latest stable release [here](https://github.com/joaomcteixeira/FarSeer-NMR/releases) or browse the project code and current state in our [GitHub repository](https://github.com/joaomcteixeira/FarSeer-NMR).

## Installation

Farseer-NMR runs on [Unix based systems](https://en.wikipedia.org/wiki/Unix). Attempting to run the current version under Windows machines will fail. Farseer-NMR has been built in its entirety using [Python](https://www.python.org/) libraries and we try to keep it up-to-date with the Python community. To install Farseer-NMR firstly:

1. Unpack the [downloaded](https://joaomcteixeira.github.io/FarSeer-NMR/#Download) version.
1. In your Terminal emulator, navigate to the unpacked Farseer-NMR folder.

There are three different ways to install Farseer-NMR according to your system setup, here are organised from the simplest to the hardest:

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

### Creating a dedicated Anaconda environment

If you use [Anaconda](https://www.anaconda.com/download/) as your Python distribution you can try to run Farseer-NMR directly, most likely all the required libraries are already installed. Alternatively, if you do not want to change your main Anaconda Python environment, you can create a secondary [Anaconda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html) dedicated to Farseer-NMR:

1. Give execution permissions to Linux_install_env.sh
```
chmod u+x Linux_install_env.sh
```
2. Run Linux_install_env.sh. This will create an Anaconda environment with all the required libraries to run Farseer-NMR inside the `envs` directory of your Anaconda installation.
```
./Linux_install_env.sh
```

### Installation for advanced users

If you are an advanced user who is proficient in manually managing your own installed Python libraries, you can get a list of the libraries required to run Farseer-NMR in the architecture respective `spec-files` in the Documention folder. Afterwards, to create the run_farseer.sh file run:

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

A Farseer-NMR calculation run can be launched without the GUI interface. Nevertheless we advocate the use of the GUI version for all users, advanced and beginners. All implemented and functional features are available through the GUI. We advice the use of the command line version only for developers. Read further in section *III.d* of the Documentation Manual.

## Documentation

We have a [Documentation folder](https://github.com/joaomcteixeira/FarSeer-NMR/tree/master/Documentation) where you can find a whole heap of helpful files along with the Full Documentation PDF. There is also an online a list of [helpful links](https://github.com/joaomcteixeira/FarSeer-NMR/wiki/Farseer-NMR-Helpful-links) to guide you in the use of Farseer-NMR.

## Tutorials and Examples

Currently we provide a [Tutorial folder](https://github.com/joaomcteixeira/FarSeer-NMR/tree/master/Documentation/Tutorial_Datasets) with artificial datasets that you can use to try out Farseer-NMR and understand its functionalities. Tutorials explanation can be found in the [Full Documentation PDF](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Farseer-NMR_Documentation.pdf).

## Participate in the Farseer-NMR community

There are several ways that you can help us improve Farseer-NMR and be part of its community! :-)  

### Reporting a bug

If you find bugs, mis-functional or non-functional features during your calculation runs, please report them by using the [Issues tab](https://github.com/joaomcteixeira/FarSeer-NMR/issues). We have prepared a set of labels that help you to specify the nature of the issues. You can use the [Issues tab](https://github.com/joaomcteixeira/FarSeer-NMR/issues) to suggest new features that you would like us to implement or that you would like help implementing.

### Become a collaborator

Help us implement new features! Do you have your own NMR analysis routines that you would like to see implemented in Farseer-NMR? You can fork the [Farseer-NMR project](https://github.com/joaomcteixeira/FarSeer-NMR) to your own GitHub account, write the functionalities and prepare a pull request for us to review and help you out! We have prepared a [Farseer coding style guide](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Code_Style_Guide_for_Developers.md) for developers so that we keep code readability consistent. We kindly request that contributors to the project adhere to this style guide.

Even if you're not an experienced programmer, please get contact with us and we will be happy join forces with you to introduce your functionalities!

### Mailing list

Post on our [mailing list](https://groups.google.com/forum/#!forum/farseer-nmr) for questions, discussion and help!

## Social Network

Find us on [Research Gate](https://www.researchgate.net/project/Farseer-NMR-automatic-treatment-and-plotting-of-large-scale-NMR-titration-data) and on [Twitter](https://twitter.com/farseer_nmr)!

## License

The entire Farseer-NMR code base comes with no liability and is licensed under the [GPL-3.0](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/COPYING).

<a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/GPLv3_Logo.svg/1200px-GPLv3_Logo.svg.png" width="75" height="37"></a>
