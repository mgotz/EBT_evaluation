# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FilmScanMain_QtDesign.ui'
#
# Created: Tue Feb 07 21:17:09 2017
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(852, 737)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.scanTab = QtGui.QWidget()
        self.scanTab.setObjectName(_fromUtf8("scanTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.scanTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter = QtGui.QSplitter(self.scanTab)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.imageLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.imageLayout.setMargin(0)
        self.imageLayout.setObjectName(_fromUtf8("imageLayout"))
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_2.addWidget(self.label_7)
        self.imagePath = QtGui.QLineEdit(self.layoutWidget1)
        self.imagePath.setObjectName(_fromUtf8("imagePath"))
        self.horizontalLayout_2.addWidget(self.imagePath)
        self.browseImageButton = QtGui.QPushButton(self.layoutWidget1)
        self.browseImageButton.setObjectName(_fromUtf8("browseImageButton"))
        self.horizontalLayout_2.addWidget(self.browseImageButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.loadButton = QtGui.QPushButton(self.layoutWidget1)
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.verticalLayout_4.addWidget(self.loadButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, 0, -1, -1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.y0 = QtGui.QSpinBox(self.layoutWidget1)
        self.y0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y0.setObjectName(_fromUtf8("y0"))
        self.gridLayout_2.addWidget(self.y0, 0, 4, 1, 1)
        self.x0 = QtGui.QSpinBox(self.layoutWidget1)
        self.x0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x0.setObjectName(_fromUtf8("x0"))
        self.gridLayout_2.addWidget(self.x0, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.x1 = QtGui.QSpinBox(self.layoutWidget1)
        self.x1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x1.setObjectName(_fromUtf8("x1"))
        self.gridLayout_2.addWidget(self.x1, 1, 2, 1, 1)
        self.y1 = QtGui.QSpinBox(self.layoutWidget1)
        self.y1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y1.setObjectName(_fromUtf8("y1"))
        self.gridLayout_2.addWidget(self.y1, 1, 4, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 1, 3, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.line_2 = QtGui.QFrame(self.layoutWidget1)
        self.line_2.setLineWidth(5)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_4.addWidget(self.line_2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_9 = QtGui.QLabel(self.layoutWidget1)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_6.addWidget(self.label_9)
        self.channel_selection = QtGui.QComboBox(self.layoutWidget1)
        self.channel_selection.setObjectName(_fromUtf8("channel_selection"))
        self.horizontalLayout_6.addWidget(self.channel_selection)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.calcStatsButton = QtGui.QPushButton(self.layoutWidget1)
        self.calcStatsButton.setObjectName(_fromUtf8("calcStatsButton"))
        self.horizontalLayout_7.addWidget(self.calcStatsButton)
        self.showHistoButton = QtGui.QPushButton(self.layoutWidget1)
        self.showHistoButton.setObjectName(_fromUtf8("showHistoButton"))
        self.horizontalLayout_7.addWidget(self.showHistoButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.line = QtGui.QFrame(self.layoutWidget1)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_4.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_6 = QtGui.QLabel(self.layoutWidget1)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.calibration_selection = QtGui.QComboBox(self.layoutWidget1)
        self.calibration_selection.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.calibration_selection.setObjectName(_fromUtf8("calibration_selection"))
        self.horizontalLayout.addWidget(self.calibration_selection)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_3.addWidget(self.label_8)
        self.DPI = QtGui.QSpinBox(self.layoutWidget1)
        self.DPI.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DPI.setMaximum(65536)
        self.DPI.setObjectName(_fromUtf8("DPI"))
        self.horizontalLayout_3.addWidget(self.DPI)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_10 = QtGui.QLabel(self.layoutWidget1)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_8.addWidget(self.label_10)
        self.phi0 = QtGui.QSpinBox(self.layoutWidget1)
        self.phi0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.phi0.setMaximum(255)
        self.phi0.setObjectName(_fromUtf8("phi0"))
        self.horizontalLayout_8.addWidget(self.phi0)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.showDose_button = QtGui.QPushButton(self.layoutWidget1)
        self.showDose_button.setObjectName(_fromUtf8("showDose_button"))
        self.verticalLayout_4.addWidget(self.showDose_button)
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.scanTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 852, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setObjectName(_fromUtf8("menuMenu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionScan_View_Settings = QtGui.QAction(MainWindow)
        self.actionScan_View_Settings.setObjectName(_fromUtf8("actionScan_View_Settings"))
        self.actionShow_Scan = QtGui.QAction(MainWindow)
        self.actionShow_Scan.setObjectName(_fromUtf8("actionShow_Scan"))
        self.actionShow_Log = QtGui.QAction(MainWindow)
        self.actionShow_Log.setObjectName(_fromUtf8("actionShow_Log"))
        self.actionDose_View_Settings = QtGui.QAction(MainWindow)
        self.actionDose_View_Settings.setObjectName(_fromUtf8("actionDose_View_Settings"))
        self.menuMenu.addAction(self.actionShow_Scan)
        self.menuMenu.addAction(self.actionShow_Log)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionScan_View_Settings)
        self.menuMenu.addAction(self.actionDose_View_Settings)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionClose)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.calibration_selection.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.imagePath, self.browseImageButton)
        MainWindow.setTabOrder(self.browseImageButton, self.loadButton)
        MainWindow.setTabOrder(self.loadButton, self.x0)
        MainWindow.setTabOrder(self.x0, self.y0)
        MainWindow.setTabOrder(self.y0, self.x1)
        MainWindow.setTabOrder(self.x1, self.y1)
        MainWindow.setTabOrder(self.y1, self.channel_selection)
        MainWindow.setTabOrder(self.channel_selection, self.calcStatsButton)
        MainWindow.setTabOrder(self.calcStatsButton, self.showHistoButton)
        MainWindow.setTabOrder(self.showHistoButton, self.calibration_selection)
        MainWindow.setTabOrder(self.calibration_selection, self.DPI)
        MainWindow.setTabOrder(self.DPI, self.phi0)
        MainWindow.setTabOrder(self.phi0, self.showDose_button)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Film Auswertung", None))
        self.label_7.setText(_translate("MainWindow", "scanned film:", None))
        self.browseImageButton.setText(_translate("MainWindow", "browse", None))
        self.loadButton.setText(_translate("MainWindow", "load image", None))
        self.label_5.setText(_translate("MainWindow", "selection coordinates:", None))
        self.label.setText(_translate("MainWindow", "x0", None))
        self.label_2.setText(_translate("MainWindow", "x1", None))
        self.label_3.setText(_translate("MainWindow", "y0", None))
        self.label_4.setText(_translate("MainWindow", "y1", None))
        self.label_9.setText(_translate("MainWindow", "color channel", None))
        self.channel_selection.setToolTip(_translate("MainWindow", "select the color channel to perform statistics on (not used for dose calculation)", None))
        self.calcStatsButton.setToolTip(_translate("MainWindow", "calculate some statistics and print to logging window", None))
        self.calcStatsButton.setText(_translate("MainWindow", "simple area stats", None))
        self.showHistoButton.setToolTip(_translate("MainWindow", "show a histogram of the selected area and channel", None))
        self.showHistoButton.setText(_translate("MainWindow", "show histogram", None))
        self.label_6.setText(_translate("MainWindow", "calibration", None))
        self.label_8.setText(_translate("MainWindow", "DPI", None))
        self.DPI.setToolTip(_translate("MainWindow", "give the resolution of the image in dots per inch to calculate a cm scale", None))
        self.label_10.setText(_translate("MainWindow", "phi 0", None))
        self.phi0.setToolTip(_translate("MainWindow", "give the pixel value that corresponds to 0 dose, in order to calculate the optical density", None))
        self.showDose_button.setToolTip(_translate("MainWindow", "calculate the dose for the selected area", None))
        self.showDose_button.setText(_translate("MainWindow", "show dose", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scanTab), _translate("MainWindow", "scan view", None))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionScan_View_Settings.setText(_translate("MainWindow", "Scan View Setting", None))
        self.actionShow_Scan.setText(_translate("MainWindow", "Show Scan Tab", None))
        self.actionShow_Log.setText(_translate("MainWindow", "Show Log", None))
        self.actionDose_View_Settings.setText(_translate("MainWindow", "Dose View Settings", None))

