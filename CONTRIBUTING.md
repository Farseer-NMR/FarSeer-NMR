# How to contribute

## Bugs and suggestions

- Report bugs and suggestions in the [issues tab](https://github.com/Farseer-NMR/FarSeer-NMR/issues), use TAGS as appropriate.
- Or, alternatively, to our mailing list farseer-nmr@googlegroups.com

## Guide to Developers

Please read our [Guide to Developers](https://github.com/Farseer-NMR/FarSeer-NMR/wiki/guide-to-developers), where you will find information regarding Coding Style and detailed documenation on the Farseer-NMR architecture.

## Pull Request

- **Always** submit a Pull Request from a cloned or forked repository of Farseer-NMR.
- Pull Requests title should start with a proposal of version change and, if helpful, followed by a short title: `v1.3.12 - corrected bar color bug in barplot`
  - follow versioning standards: [_major/visible_ [ _new feature_ [ _bug correction_]]
  - new version number should be updated in `install/system.py`.
  - be nice and update the installation banner at `install/messages.py` using this ASCII text generator, just change the version number in the following link `:-)`:
```
                                                                                    here
                                                                                    |||||
http://patorjk.com/software/taag/#p=display&h=1&f=Doom&t=---------%0AFarSeer-NMR%0Av1.3.0%0A---------
```

- Pull Request description should state the added improvements and corrections.
- Pull Request should close issues whenever applicable.

_Thanks!_
