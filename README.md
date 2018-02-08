# Welcome to Farseer-NMR

A full, community driven and ever growing suite to analyse **peaklist files** extracted from multivariable series of biomolecular NMR experiments. Up to three different experimental variables can be combined and analysed together.  
With Farseer-NMR you can automatically calculate structural parameters from the peaklist dataset which are then comprehensively and conveniently represented in publication-ready plots.

Conviniently save and load you configuration files and rerun your operations with one-click!

Full traceability via [Markdown](https://en.wikipedia.org/wiki/Markdown) formatted log file.

![FarSeer Banner](https://github.com/joaomcteixeira/FarSeer-NMR/blob/master/Documentation/Figures/FS_banner.png?raw=true)

## Requierements and Configuration

Farseer-NMR runs on [Unix based systems](https://en.wikipedia.org/wiki/Unix). Under the current version, attempting to run it on Windows machines will fail.  
Farseer-NMR runs enterily on [Python](https://www.python.org/) libraries and we try to keep it up-to-date with the Python community. We advice you to install and manage your Python packages with [Anaconda](https://www.anaconda.com/download/).  
In case there is a library incompatibility, you can find the [spec-files under the Documentation folder](https://github.com/joaomcteixeira/FarSeer-NMR/tree/master/Documentation) to create [Anaconda environments](https://conda.io/docs/user-guide/tasks/manage-environments.html) in your computer in order to run Farseer-NMR.

## Running

There are two ways to run Farseer-NMR: using the fully featured user interface (GUI) or directly on the ```Terminal``` emulator. There is no advantage for running Farseer-NMR directly in the command line instead of using the GUI version. The GUI is fully featured and all functional features can be configured under the specially designed menus; only under development features are kept solely in the Core (terminal version) and can be accessed (if available) by direct editing the JSON config file.  

We **strongly** advice users to run the GUI version.  

### Using the GUI

Using the GUI is as simple as running the main GUI file through Python.

```
python main.py
```

### Via terminal

```
python core/farseemain.py <path to calculation folder> <path to conf.json file>
```

where ```calculation folder``` is the folder containing the hierarchic spectra/ folder. Consider the GUI will create the spectra/ folder for you while via terminal you have to create it your own.

### Chaging the config file

Alternatively, you can always change the configuration file mannually by editing the .json file and Load your configuration via GUI and continue from there. Anyway, we don't see a point in doing this instead of using the GUI. :-P

## License

The whole Farseer-NMR comes with no liability and is licensed under the GPL-3.0.

<a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/GPLv3_Logo.svg/1200px-GPLv3_Logo.svg.png" width="75" height="37"></a>
