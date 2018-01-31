#enusre usage of PyQt4 and avoid something using PyQt5 instead
#a perfect, future version would be able to use either PyQt4 or PyQt5
import os
#enable compatibility to both pyqt4 and pyqt5 and load the proper modules
_modname = os.environ.setdefault('QT_API', 'pyqt')
assert _modname in ('pyqt', 'pyqt5')


from matplotlib import use
    

if os.environ['QT_API'] == 'pyqt5':
    use("Qt5Agg", warn=False) #set the matplotlib backend and don't warn if already set

else:
    #ensure API v2 for pyqt (native python data types) pyqt5 only offers this
    #API, therefore its not needed there
    import sip
    API_NAMES = ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", 
                 "QVariant")
    API_VERSION = 2
    for name in API_NAMES:
        sip.setapi(name, API_VERSION)
    

    use("Qt4Agg", warn=False) #set the matplotlib backend and don't warn if already set

        
        

#make those Classes available in the base namespace
from .navtoolbar import MyNavigationToolbar
if os.environ['QT_API'] == 'pyqt5':
    from .main_ui_qt5 import Ui_MainWindow
else:
    from .main_ui_qt4 import Ui_MainWindow