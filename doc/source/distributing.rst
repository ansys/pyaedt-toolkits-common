==========
Distribute
==========
Distributing your application in a distributable format means packaging it in a way that makes it easy to install, run
and share. A distributable format bundles everything needed (dependencies, configurations, executables) into a
convenient package.
Packaging helps making your toolkit easier to distribute and more likely to run consistently across systems.

How to distribute in Windows
---------------------------
The aim is to package the toolkit into a Windows installer (EXE file) using NSIS (Nullsoft Scriptable Install System).

Pre-requisites and setup
^^^^^^^^^^^^^^^^^^^^^^^^
1. Install chocolatey (Windows package manager)
Chocolatey lets you install tools like NSIS easily. For example, you can install NSIS by:
- Opening a PowerShell terminal as Administrator.
- Running the following command

.. code:: powershell

    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

Visit the `Chocolatey website <https://chocolatey.org/install>`_ for more information on the installation process.

2. Add NSIS to your PATH in Windows environment variables
Usually the NSIS is located at ``C:\Program Files (x86)\NSIS``.

3. Install NSIS using chocolatey

.. code:: powershell

    choco install nsis -y

4. Install PyInstaller
PyInstaller bundles a Python application and all its dependencies into a single package.
The user can run the packaged app without installing a Python interpreter or any modules.

This step requires the toolkit TOML file to have a section called ``freeze`` in ``[project.optional-dependencies]``.
An example can be found in `Antenna Wizard TOML file <https://github.com/ansys/pyaedt-toolkits-antenna/blob/main/pyproject.toml#L30>`_.

Open the toolkit project in your IDE of choice, activate your virtual environment and run the following command:

.. code::

    pip install .[freeze]

5. Extract the toolkit version
This step requires you to have the `extract_version.py <https://github.com/ansys/pyaedt-toolkits-antenna/blob/main/installer/extract_version.py>`_ python script.

.. code::

    python installer/extract_version.py

6. Create the standalone executable
This step requires you to have a `frozen.spec` file. An example of such file can be found  `here <https://github.com/ansys/pyaedt-toolkits-antenna/blob/main/frozen.spec>`_.
This file plays a key role in how your toolkit is turned into a standalone executable.
It defines the instructions PyInstaller uses to package your toolkit into a single executable file.

.. code::

    pyinstaller frozen.spec

7. Create a standalone installer program
This step requires you to have a `setup.nsi` file. An example of such file can be found `here <https://github.com/ansys/pyaedt-toolkits-antenna/blob/main/setup.nsi>`_.
The ``setup.nsi`` file is the NSIS script (a plain text file) that describes how to build the installer, that is what files to include,
where to install them, shortcuts to create, etc., and it compiles this script into a Windows installer executable.
In simple terms ``setup.nsi`` contains instructions and by running:

.. code::

    makensis setup.nsi

NSIS turns these instructions into a standalone installer program.
