============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. You can contribute
from the scope of an user or as a core Python developer.

Reporting and Requesting
========================

Bug reports
-----------

When `reporting a bug <https://github.com/Farseer-NMR/FarSeer-NMR/issues>`_ please use one of the provided issue templates if applicable, otherwise just start a blank issue and describe your situation.

Documentation improvements
--------------------------

FarSeer-NMR could always use more documentation, whether as part of the
official FarSeer-NMR docs, in docstrings, or even on the web in blog posts,
articles, and such. Write us a *documentation* `issue <https://github.com/Farseer-NMR/FarSeer-NMR/issues/new/choose>`_ describing what you
would like to see improved in the documentation, and if you can do
it just `Pull Request <https://github.com/Farseer-NMR/FarSeer-NMR/pulls>`_ your proposed updates. 

Feature requests and feedback
-----------------------------

The best way to send feedback is to file an issue at https://github.com/Farseer-NMR/FarSeer-NMR/issues/new/choose using the *feature* template.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that code contributions are welcome :)

Code Development
================

To contribute to the development of *FarSeer-NMR*:

1. Fork the FarSeer-NMR repository.
2. Clone your fork to your local machine::

    git clone https://github.com/YOUR-USER-NAME/FarSeer-NMR.git <destination folder> 

3. Set up a new Python environment for the development of FarSeer-NMR so that the development version does not conflict with the production installation.

3.1 If you use Anaconda as your Python package manager do::

    conda env create -f requirements_conda.yml

3.2 If you are using PyPI as your package manager follow `this instructions <https://docs.python.org/3/tutorial/venv.html>`_.

4. Remember to activate the new environment before proceeding to the installation, with Anaconda: ``conda activate farseernmrdev``.

5. Install FarSeer-NMR in the development mode, from within your fork folder::

    python setup.py develop

This ensures that the FarSeer-NMR version running in your development environment is the source in your git folder.

6. *FarSeer-NMR* relies on `tox <https://tox.readthedocs.io/en/latest/>`_ to orchestrate testing environments, ensuring correct collaborative development, install ``tox``::

    # with Anaconda
    conda install -c conda-forge tox
    
    # with PyPI
    pip install tox

5. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

5.1 Now you can make your changes locally.

6. When you're done making changes run all the checks and docs builder with **tox** one command::

    tox

6.1. If all tests pass you are set to go :-)``

7. Commit your changes and push your branch to your *FarSeer-NMR fork* on GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

8. `Submit a pull request through the GitHub website <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request>`_.

9. To keep you fork repository updated with the main repository latest changes::

    # move to the master branch
    git checkout master

    # add a reference to the upstream repository
    # this is the main FarSeer-NMR repository
    # you only have to do this once
    git remote add upstream https://github.com/Farseer-NMR/FarSeer-NMR

    # fetch the latest code from the main repository
    git fetch upstream

    # merge those changes to your master branch
    git pull upstream master

    # push to you online repository the new changes
    # so that your fork synchronizes with the main
    git push origin master

10. To continue developing a new feature just repeat from steps 5.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make a pull request.

For merging, you should:

1. Include passing tests (run ``tox``) [1]_.
2. Update documentation when there's new API, functionality etc.
3. Add a note to ``CHANGELOG.rst`` about the changes.
4. Add yourself to ``AUTHORS.rst``.

.. [1] If you don't have all the necessary python versions available locally you can rely on Travis - it will
       `run the tests <https://travis-ci.org/Farseer-NMR/FarSeer-NMR/pull_requests>`_ for each change you add in the pull request.

       It will be slower though ...

Tips
----

You can run individual test environment with tox, for example, to test lint::

    tox -e check 

to test documentation::

    tox -e docs

to perform coverage-reported tests::

    tox -e py38

Continuous Integration
======================

This project follows Continuous Integration (CI) good practices (let us know if something can be improved). As referred in the previous section, testing environment is provided by `tox <https://tox.readthedocs.io/en/latest/>`_. All *tox* testing environments run on `Travis-CI <https://travis-ci.org/Farseer-NMR/FarSeer-NMR>`_; there, we check for code style, code quality, documentation, tests and test coverage. If you want to know more, tox testing configuration is defined in the `tox.ini <https://github.com/Farseer-NMR/FarSeer-NMR/blob/master/tox.ini>`_ file.
