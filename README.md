# EBT_evaluation

## A tool to calculate dose from scanned EBT films

It provides an ebttools.core where you can find classes and functions to calculate dose arrays from scanned images.
If you want to write your own script, this is where you should look.
In addition, there is GUI, which is run from the gui.main.run, with the run.py or from the installed script/executable.

## Installation

The GUI is built on PyQt, PyQt4 and PyQt5 both should work. 
However, at least PyQt4 can not be specified as a real dependency because it is not on PyPi.
Therefore, you should take care of installing those beforehand.
Most Python installations should come with one of them installed, as the Spyder IDE also uses it.

### Manual

I wrote a setup.py to ease installation. 
However, it has proven difficult to make this work reliably in all possible environments.
In particular, the challanges have been very old Python installations (PythonXY), Windows environment in general (no direct installation of e.g. numpy through PyPi) and specifically Windows with restricted permissions.

So the manual way may be the most robust way to use/install EBT_evaluation (and not give you false hope of an easy installation)
To this end make sure you have PyQt, pillow, SciPy, NumPy, matplotlib and formlayout installed.
On Python2.7 also future and configparser.
Then also download the PyGUITools and PyDataProcessing repositories and copy the *mg* folder into the EBT_evaluation folder, such that ebttools and mg are in the same folder.
Then run the run.py and install any modules it can't find.

If you want to use the core modules from another script, simply add the EBT_evaluation directory to you pythonpath.

### "Automated"

If you use conda (probably the best way to go on Windows) it's best if you install the dependencies through conda, before installing EBT_evaluation.
This is because the EBT_evalauation whill use pip to resolve its dependencies and you will end up with a mix of conda and pip packages.
Use 
> conda install --yes --file conda_requirements.txt

to install all the conda available packages.

Subesquently, download EBT_evaluation and switch to the extracted directory. Then run 
> pip install . --process-dependency-links --allow-all-external

This will trigger a depreciation warning, but there is no other way for external dependencies and it has been depreciated but not removed for several years.
It should install the EBT_evaluation and all its dependencies, including my own modules from github.
If your installation uses pip to manage all of pyhton, i.e., you are on Linux, then this command alone should do it all, no need for the conda_requirements.txt.

If you installed the conda_requirements beforehand this should only pull mg_* modules and the formlayout modules. 
If it installs additional stuff through pip then you may want to uninstall those modules with pip and reinstall them using conda.

In addition, the installation will create a script/executable called *EBT-evaluation*.
You can use this script/executable to directly run the GUI, on Linux just call EBT-evaluation from the terminal, on Winows the .exe should be in python-directory/Scripts.

If pip is somehow unavailable
> easy_install .

should also work or
> python setup.py install

However, pip is most likely to get all the dependencies correctly figured out.

If none of these work, you can also download the dependencies manually and install them.
Get the PyGUITools and PyDataProcessing repositories from my github and install them using their respective setup.py.
Then install the EBTtools and resolve all other dependencies.
