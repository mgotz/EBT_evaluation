# EBT_evaluation

## A tool to calculate dose from scanned EBT films

It provides an ebttools.core where you can find classes and functions to calculate dose arrays from scanned images.
If you want to write your own script, this is where you should look.
In addition, there is GUI, which is run from the gui.main.run, with the run.py or from the installed script/executable.

## Installation

The GUI is built on PyQt4, which can not be specified as a real dependency because it is not on PyPi.
It requires a working Qt4 installation and needs to be installed via system repositories.
Most python instalations should come with it as spyder also uses it, but maybe very recent installations forgo it for the newer PyQt5, which offers more flexible licensing.
Maybe a future version will also support PyQt5 or PySide, but at the moment this only works with PyQt4.

Download and switch to the extracted directory. Then run 
> pip install . --process-dependency-links --allow-all-external
This will trigger a depreciation warning, but there is no other way for external dependencies and it has been depreciated but not removed for several years.
It should install the EBT_evaluation and all its dependencies, including my own modules from github.
In addition it will create a script/executable called *EBT-evaluation*.
You can use this script/executable to directly run the GUI, on Linux just call EBT-evaluation from the terminal, on Winows the .exe should be in python-directory/Scripts.

If pip is somehow unavailable
> easy_install .
should also work or
> python setup.py install
However, pip is most likely to get all the dependencies correctly figured out.

If non of these work, you can also download the dependencies manually and install them.
Get the PyGUITools and PyDataProcessing repositories from my github and install them using their respective setup.py.
Then install the EBTtools and resolbe all other dependencies, primarily those should be PyQt4, matplotlib, scipy and pillow.
The GUI can be run using the creaed *EBT-evaluation* script/executable or using the run.py.

If all fails, copy the mg directories in those repositories into the same directory as the run.py and then it should find what it needs.