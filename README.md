# Welcome to Farseer-NMR

A fully community driven and ever growing suite to analyse **peaklist files** extracted from multivariable series of biomolecular NMR experiments. Up to three different experimental variables can be combined and analysed together.  
With Farseer-NMR, you can automatically calculate structural parameters from peaklist datasets, which are then comprehensively and conveniently represented in publication-ready plots.

Conveniently save and load your configuration files and re-run your operations with one-click!

Full traceability via [Markdown](https://en.wikipedia.org/wiki/Markdown) formatted log file.

![FarSeer Banner](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Figures/FS_banner.png?raw=true)

## Requirements and Configuration

Farseer-NMR runs on [Unix based systems](https://en.wikipedia.org/wiki/Unix). Attempting to run the current version under Windows machines will fail.  
Farseer-NMR has been built in its entirety using [Python](https://www.python.org/) libraries and we try to keep it up-to-date with the Python community. We advise you to install and manage your Python packages with [Anaconda](https://www.anaconda.com/download/).  
In the case of a library incompatibility, you can find the [spec-files under the Documentation folder](https://github.com/joaomcteixeira/FarSeer-NMR/tree/master/Documentation) required to create [Anaconda environments](https://conda.io/docs/user-guide/tasks/manage-environments.html) on your computer in order to run Farseer-NMR.

## Running

There are two ways to run Farseer-NMR: using the fully featured graphical user interface (GUI) or directly in a ```Terminal``` emulator. There are no advantages to running Farseer-NMR directly on the command line, rather than using the GUI version. All released features can be configured using the GUI; only under development features are kept solely in the Core (terminal version) and can be accessed (if available) by direct editing the JSON config file.

We **strongly** advise users to run the GUI version.  

### Using the GUI

Using the GUI is as simple as running the main GUI file through Python.

```
python main.py
```

### Via terminal

```
python core/farseemain.py <path to calculation folder> <path to conf.json file>
```

where ```calculation folder``` is the folder containing the hierarchical spectra/ folder. The GUI will create the spectra/ folder for you automatically, whereas to run Farseer-NMR via the terminal you have to create it yourself.

### Changing the config file

Alternatively, you can always change the calculation settings manually by editing the .json configuration file, loading your configuration via GUI and continue from there. Anyway, we don't see a point in doing this rather than using the GUI. :-P

## Documentation

We have a [Documentation folder](https://github.com/joaomcteixeira/FarSeer-NMR/tree/master/Documentation) where you can find a whole hand of helpful files. Also, there's an online [Wiki](https://github.com/joaomcteixeira/FarSeer-NMR/wiki) page with additional links and info regard Farseer-NMR Documentation. These pages are dynamic upgraded according to the project/community needs.

## Participate in the Farseer-NMR community

You can help us to improve in several ways and be part of our community! :-)  

### Reporting a bug

If you find bugs or unfunctional features during your runs, report them in the [Issues tab](https://github.com/joaomcteixeira/FarSeer-NMR/issues). We have prepared a set of labels that help to identify the issues accordingly. Also, you can use Issues to suggest new features.

### Become a collaborator

Help us implementing new features! Do you have your own NMR analysis routines that you would like to see implemented in Farseer-NMR? You can fork this project to your own GitHub account, do the implementation and prepare a pull request for us to review and help you out! We have prepared a [Farseer coding style guid](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Code_Style_Guide_for_Developers.md) for developers so that we keep code readability consistent.

In case you don't have coding expericience, please let us know and we will be happy join forces with you to bring about the functionalities!

### Mailing list

Post on our [mailing list](https://groups.google.com/forum/#!forum/farseer-nmr) for questions, discussion and help!

## Social Network

Find us on [Research Gate](https://www.researchgate.net/project/Farseer-NMR-automatic-treatment-and-plotting-of-large-scale-NMR-titration-data) and on [Twitter]!

## License

The entire Farseer-NMR code base comes with no liability and is licensed under the GPL-3.0.

<a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/GPLv3_Logo.svg/1200px-GPLv3_Logo.svg.png" width="75" height="37"></a>
