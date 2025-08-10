==========
Contribute
==========
Overall guidance on contributing to a PyAnsys repository appears in
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyAEDT or its toolkits.

The following contribution information is specific to this library.

Clone the repository
--------------------
To clone and install the latest version of the PyAEDT Common Toolkit in
development mode, run these commands:

.. code::

    git clone https://github.com/ansys/pyaedt-toolkits-common.git
    cd pyaedt-toolkits-common
    python -m pip install --upgrade pip
    pip install -e .[all]

Post issues
-----------
Use the `PyAEDT Common Toolkit Issues <https://github.com/ansys/pyaedt-toolkits-common/issues>`_ page
to create issues to report bugs and request new features.

View documentation
-------------------
Documentation for the latest stable release is hosted at `PyAEDT Common Toolkit documentation <https://aedt.common.toolkit.docs.pyansys.com/version/stable/>`_.

In the upper right corner of the documentation’s title bar, there is an option for switching from viewing
the documentation for the latest stable release to viewing the documentation for the development version
or previously released versions.

Adhere to code style
--------------------
The Common Toolkit is compliant with `PyAnsys code style
<https://dev.docs.pyansys.com/coding-style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to select the code style.

You can install and activate this tool with these commands:

.. code:: bash

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook with this command:

.. code:: bash

  pre-commit install

This way, it's not possible for you to push code that fails the style checks::

  $ pre-commit install
  $ git commit -am "Add my cool feature."
  black....................................................................Passed
  isort (python)...........................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  fix requirements.txt.....................................................Passed
  blacken-docs.............................................................Passed

Maximum line length
~~~~~~~~~~~~~~~~~~~
Best practice is to keep the line length at or below 120 characters for code
and comments. Lines longer than this might not display properly on some terminals
and tools or might be difficult to follow.
