Installation
============

The pyGLV can be installed via the standard mechanisms for Python packages, and is available through PyPI for standalone use, 
or Github, for development. We strongly propose to **install and use** pyGLV within a new environment created via ``conda``.


Creating a Conda Environment
------------------------------
After downloading the proper 
`Anaconda python distribution <https://www.anaconda.com/distribution/#download-section>`_, 
based on your system you may create a virtual environment via the ``conda`` command.

Typically, you may create a new envirnment via the command::

    conda create -n myenv python==3.8

This creates a new environment, named myenv, with a python version 3.8, which is the proper version to run pyGLV.

You may now activate the environment by running::

    conda activate myenv

When finished, you may deactivate it by running::

    conda deactivate

Installing pyECSS
--------------------

.. note ::
    In order to install and use pyGLV, the package ``pyECSS`` must be installed. 

You may install it 

* via ``pip3`` for standalone use (**latest stable version**) ::
    
    pip3 install pyECSS

* via git clone for standalone use (**latest dev version**)::

    pip3 install git+https://github.com/papagiannakis/pyECSS.git

* via git clone and editable (``-e``) install, for development::

    git clone https://github.com/papagiannakis/pyECSS.git
    pip3 install -e ./pyECSS

More information on the pyECSS `homepage <https://github.com/papagiannakis/pyECSS>`_.



Stable Version - Standalone Use
--------------------------------
For standalone use, you may install pyGLV, via ``pip3`` ::

    pip3 install pyGLV

.. note ::

    The version installed via pip3 may be a few versions behind the current version in development. 
    If you need to test the latest version, you should install it via ``git`` and local install.

Latest Version - Standalone Use
----------------------------------

If you want the latest (development) version of ``pyGLV`` you can locally pip install it from the latest develop branch with::

    pip3 install git+https://github.com/papagiannakis/pyGLV.git

Latest Version - For development
-----------------------------------

If you want to modify ``pyGLV`` itself, then you should use an editable (``-e``) installation::

    git clone https://github.com/papagiannakis/pyGLV.git
    pip3 install -e ./pyGLV

The proper way to contribute is to fork the `develop branch <https://github.com/papagiannakis/pyGLV.git>`_ , 
clone it to your computer and run::

    pip3 install -e .

at the directory where the `setup.py` file is located. 
You should then work on a feature branch and open a pull request, when you see fit. 
