.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/aj-cloete/pssa/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Singular Spectrum Analysis could always use more documentation, whether as part of the
official Singular Spectrum Analysis docs and in docstrings.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/aj-cloete/pssa/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

Get Started!
------------

Ready to contribute? Here's how to set up `pssa` for local development.

1. Clone the `pssa` repo on GitHub.::

    git clone git@github.com:aj-cloete/pssa.git

2. Create a pipenv environment (assuming you have the `basics <https://github.com/aj-cloete/pipenv-cookiecutter/blob/master/the_basics.md>`_ covered) ::

    cd pssa
    pipenv install --dev
    pipenv run pre-commit install

3. Activate your environment shell. ::

    pipenv shell

4. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass all the tests by running::

    pipenv run pytest
    pipenv run pytest --cov --cov-fail-under=100
    pipenv run pipenv check

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6+

Tips
----

You can check the command next to each of the **entry:** lines in `this file </.pre-commit-config.yaml>`_ to understand what each of the individual pre-commit hooks runs.

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

  bumpversion patch # possible: major / minor / patch
  git push
  git push --tags
