#enusre usage of PyQt4 and avoid something using PyQt5 instead
#a perfect, future version would be able to use either PyQt4 or PyQt5
import os
import sip
API_NAMES = ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", 
             "QVariant")
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)

#make sure other modules use pyqt4 as well (you cant mix qt versions)
os.environ["QT_API"] = 'pyqt'
#plotting with matplotlib, must also use PyQt4
from matplotlib import use
use("Qt4Agg")

#make those Classes available in the base namespace
from .navtoolbar import MyNavigationToolbar
from main_ui import Ui_MainWindow