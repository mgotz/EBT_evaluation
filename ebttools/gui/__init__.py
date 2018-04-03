import os
import warnings

defaultAPI = 'pyqt'

#ensure API v2 for pyqt (native python data types) pyqt5 only offers this API
#hopefully setting it for PyQt5 does not cause errors
import sip
RequiredAPINames = ("QVariant","QString") #those I definitly use
OptionalAPINames = ("QDate", "QDateTime", "QTextStream", "QTime", "QUrl") #those I may in the future

API_VERSION = 2

for name in RequiredAPINames:
	sip.setapi(name, API_VERSION)
for name in OptionalAPINames:
    try:
        sip.setapi(name, API_VERSION)
    except ValueError:
        warnings.warn("failed to set {!s} to API v2".format(name),ImportWarning)

#check whether an environment variable is set to choose pyqt version.
#If not try what is installed and set the default
if not "QT_API" in os.environ:
	try:
		import PyQt4
		defaultAPI = 'pyqt'
	except ImportError:
		try:
			import PyQt5
			defaultAPI = 'pyqt5'
		except ImportError:
			raise ImportError("The EBT GUI needs either PyQt4 or PyQt5 and neither was found")

#set the environment variable and ensure that it was either pyqt or pyqt5
_modname = os.environ.setdefault('QT_API', defaultAPI)
assert _modname in ('pyqt', 'pyqt4', 'pyqt5')

from matplotlib import use

if os.environ['QT_API'] == 'pyqt5':
    use("Qt5Agg", warn=False) #set the matplotlib backend and don't warn if already set

else:
    use("Qt4Agg", warn=False) #set the matplotlib backend and don't warn if already set

        
        

#make those Classes available in the base namespace
from .navtoolbar import MyNavigationToolbar
if os.environ['QT_API'] == 'pyqt5':
    from .main_ui_qt5 import Ui_MainWindow
else:
    from .main_ui_qt4 import Ui_MainWindow