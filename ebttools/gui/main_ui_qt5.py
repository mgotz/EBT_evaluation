# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_QtDesign.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(852, 737)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.scanTab = QtWidgets.QWidget()
        self.scanTab.setObjectName("scanTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scanTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(self.scanTab)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.imageLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.imageLayout.setContentsMargins(0, 0, 0, 0)
        self.imageLayout.setObjectName("imageLayout")
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.imagePath = QtWidgets.QLineEdit(self.layoutWidget1)
        self.imagePath.setObjectName("imagePath")
        self.horizontalLayout_2.addWidget(self.imagePath)
        self.browseImageButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.browseImageButton.setObjectName("browseImageButton")
        self.horizontalLayout_2.addWidget(self.browseImageButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.loadButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.loadButton.setObjectName("loadButton")
        self.verticalLayout_4.addWidget(self.loadButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.line_4 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_4.setLineWidth(5)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_4.addWidget(self.line_4)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, 0, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.y0 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.y0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y0.setObjectName("y0")
        self.gridLayout_2.addWidget(self.y0, 0, 4, 1, 1)
        self.x0 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.x0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x0.setObjectName("x0")
        self.gridLayout_2.addWidget(self.x0, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.x1 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.x1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x1.setObjectName("x1")
        self.gridLayout_2.addWidget(self.x1, 1, 2, 1, 1)
        self.y1 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.y1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y1.setObjectName("y1")
        self.gridLayout_2.addWidget(self.y1, 1, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_2.setLineWidth(5)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.label_15 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_4.addWidget(self.label_15)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.channel_selection = QtWidgets.QComboBox(self.layoutWidget1)
        self.channel_selection.setObjectName("channel_selection")
        self.horizontalLayout_6.addWidget(self.channel_selection)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.calcStatsButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.calcStatsButton.setObjectName("calcStatsButton")
        self.horizontalLayout_7.addWidget(self.calcStatsButton)
        self.showHistoButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.showHistoButton.setObjectName("showHistoButton")
        self.horizontalLayout_7.addWidget(self.showHistoButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.line_3 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_3.setLineWidth(5)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_4.addWidget(self.line_3)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_4.addWidget(self.label_11)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.saveTablePath = QtWidgets.QLineEdit(self.layoutWidget1)
        self.saveTablePath.setObjectName("saveTablePath")
        self.horizontalLayout_4.addWidget(self.saveTablePath)
        self.browseSaveTable = QtWidgets.QPushButton(self.layoutWidget1)
        self.browseSaveTable.setObjectName("browseSaveTable")
        self.horizontalLayout_4.addWidget(self.browseSaveTable)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_5.addWidget(self.label_13)
        self.filmNumber = QtWidgets.QLineEdit(self.layoutWidget1)
        self.filmNumber.setObjectName("filmNumber")
        self.horizontalLayout_5.addWidget(self.filmNumber)
        self.saveChannelData = QtWidgets.QPushButton(self.layoutWidget1)
        self.saveChannelData.setObjectName("saveChannelData")
        self.horizontalLayout_5.addWidget(self.saveChannelData)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.line = QtWidgets.QFrame(self.layoutWidget1)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_4.addWidget(self.label_14)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.calibration_selection = QtWidgets.QComboBox(self.layoutWidget1)
        self.calibration_selection.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.calibration_selection.setObjectName("calibration_selection")
        self.horizontalLayout.addWidget(self.calibration_selection)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.DPI = QtWidgets.QSpinBox(self.layoutWidget1)
        self.DPI.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DPI.setMaximum(65536)
        self.DPI.setObjectName("DPI")
        self.horizontalLayout_3.addWidget(self.DPI)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.calcPhi0Button = QtWidgets.QPushButton(self.layoutWidget1)
        self.calcPhi0Button.setObjectName("calcPhi0Button")
        self.horizontalLayout_8.addWidget(self.calcPhi0Button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(0, 10, 10, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.phi0LabelCh1 = QtWidgets.QLabel(self.layoutWidget1)
        self.phi0LabelCh1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.phi0LabelCh1.setObjectName("phi0LabelCh1")
        self.horizontalLayout_9.addWidget(self.phi0LabelCh1)
        self.phi0Ch1 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.phi0Ch1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.phi0Ch1.setDecimals(3)
        self.phi0Ch1.setMaximum(255.0)
        self.phi0Ch1.setProperty("value", 255.0)
        self.phi0Ch1.setObjectName("phi0Ch1")
        self.horizontalLayout_9.addWidget(self.phi0Ch1)
        self.phi0LabelCh2 = QtWidgets.QLabel(self.layoutWidget1)
        self.phi0LabelCh2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.phi0LabelCh2.setObjectName("phi0LabelCh2")
        self.horizontalLayout_9.addWidget(self.phi0LabelCh2)
        self.phi0Ch2 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.phi0Ch2.setDecimals(3)
        self.phi0Ch2.setMaximum(255.0)
        self.phi0Ch2.setProperty("value", 255.0)
        self.phi0Ch2.setObjectName("phi0Ch2")
        self.horizontalLayout_9.addWidget(self.phi0Ch2)
        self.phi0LabelCh3 = QtWidgets.QLabel(self.layoutWidget1)
        self.phi0LabelCh3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.phi0LabelCh3.setObjectName("phi0LabelCh3")
        self.horizontalLayout_9.addWidget(self.phi0LabelCh3)
        self.phi0Ch3 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.phi0Ch3.setDecimals(3)
        self.phi0Ch3.setMaximum(255.0)
        self.phi0Ch3.setProperty("value", 255.0)
        self.phi0Ch3.setObjectName("phi0Ch3")
        self.horizontalLayout_9.addWidget(self.phi0Ch3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.showDose_button = QtWidgets.QPushButton(self.layoutWidget1)
        self.showDose_button.setObjectName("showDose_button")
        self.verticalLayout_4.addWidget(self.showDose_button)
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.scanTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 852, 19))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionScan_View_Settings = QtWidgets.QAction(MainWindow)
        self.actionScan_View_Settings.setObjectName("actionScan_View_Settings")
        self.actionShow_Scan = QtWidgets.QAction(MainWindow)
        self.actionShow_Scan.setObjectName("actionShow_Scan")
        self.actionShow_Log = QtWidgets.QAction(MainWindow)
        self.actionShow_Log.setObjectName("actionShow_Log")
        self.actionDose_View_Settings = QtWidgets.QAction(MainWindow)
        self.actionDose_View_Settings.setObjectName("actionDose_View_Settings")
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
        MainWindow.setTabOrder(self.DPI, self.showDose_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EBT evaluation"))
        self.label_7.setText(_translate("MainWindow", "scanned film:"))
        self.imagePath.setToolTip(_translate("MainWindow", "path to the file containing a scan of films"))
        self.browseImageButton.setToolTip(_translate("MainWindow", "browse, if you don\'t like typing a path"))
        self.browseImageButton.setText(_translate("MainWindow", "browse"))
        self.loadButton.setToolTip(_translate("MainWindow", "load the specified scan"))
        self.loadButton.setText(_translate("MainWindow", "load image"))
        self.label_5.setToolTip(_translate("MainWindow", "the rectangular selection is specified by the coordinates of two corners. Their order is irrelevant."))
        self.label_5.setText(_translate("MainWindow", "selection coordinates:"))
        self.label.setText(_translate("MainWindow", "x0"))
        self.label_2.setText(_translate("MainWindow", "x1"))
        self.label_3.setText(_translate("MainWindow", "y0"))
        self.label_4.setText(_translate("MainWindow", "y1"))
        self.label_15.setToolTip(_translate("MainWindow", "Use this section to cacluate some simple statistics of the selected area and the selected color channel."))
        self.label_15.setText(_translate("MainWindow", "raw statistics:"))
        self.label_9.setText(_translate("MainWindow", "color channel"))
        self.channel_selection.setToolTip(_translate("MainWindow", "select the color channel to perform statistics on (not used for dose calculation)"))
        self.calcStatsButton.setToolTip(_translate("MainWindow", "calculate some statistics and print to logging window"))
        self.calcStatsButton.setText(_translate("MainWindow", "simple area stats"))
        self.showHistoButton.setToolTip(_translate("MainWindow", "show a histogram of the selected area and channel"))
        self.showHistoButton.setText(_translate("MainWindow", "show histogram"))
        self.label_11.setToolTip(_translate("MainWindow", "Use this section to save the data (average and std) from all three color channels alongside the selection coordinates to a new line in the specified file. This is to more easily construct the tables needed for calibration."))
        self.label_11.setText(_translate("MainWindow", "export for calibration:"))
        self.label_12.setText(_translate("MainWindow", "save data to:"))
        self.saveTablePath.setToolTip(_translate("MainWindow", "Path to save the data to. Each save operation appends an new line."))
        self.browseSaveTable.setToolTip(_translate("MainWindow", "Browse for a file instead of giving the path"))
        self.browseSaveTable.setText(_translate("MainWindow", "browse"))
        self.label_13.setText(_translate("MainWindow", "film no."))
        self.filmNumber.setToolTip(_translate("MainWindow", "Give the number of the film. This is written as the first column to the save file."))
        self.saveChannelData.setToolTip(_translate("MainWindow", "Save the information relevant to construct a calibration curve to a new line in the save file. Uses only the area selected above."))
        self.saveChannelData.setText(_translate("MainWindow", "save"))
        self.label_14.setToolTip(_translate("MainWindow", "Use this section to create a dose view of the selected area, using the settings made below."))
        self.label_14.setText(_translate("MainWindow", "create a dose view:"))
        self.label_6.setText(_translate("MainWindow", "calibration"))
        self.calibration_selection.setToolTip(_translate("MainWindow", "select an appropriate calibration to calculate the dose"))
        self.label_8.setText(_translate("MainWindow", "DPI"))
        self.DPI.setToolTip(_translate("MainWindow", "give the resolution of the image in dots per inch to calculate a cm scale"))
        self.label_10.setToolTip(_translate("MainWindow", "give the pixel value that corresponds to 0 dose, in order to calculate the net optical density"))
        self.label_10.setText(_translate("MainWindow", "phi 0"))
        self.calcPhi0Button.setToolTip(_translate("MainWindow", "use the average values from the current selection as phi0"))
        self.calcPhi0Button.setText(_translate("MainWindow", "take current selection"))
        self.phi0LabelCh1.setText(_translate("MainWindow", "red:"))
        self.phi0Ch1.setToolTip(_translate("MainWindow", "red/1st channel value for 0 dose"))
        self.phi0LabelCh2.setText(_translate("MainWindow", "green:"))
        self.phi0Ch2.setToolTip(_translate("MainWindow", "green/2nd channel value for 0 dose"))
        self.phi0LabelCh3.setText(_translate("MainWindow", "blue:"))
        self.phi0Ch3.setToolTip(_translate("MainWindow", "blue/3rd channel value for 0 dose"))
        self.showDose_button.setToolTip(_translate("MainWindow", "calculate the dose for the selected area"))
        self.showDose_button.setText(_translate("MainWindow", "show dose"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scanTab), _translate("MainWindow", "scan view"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionScan_View_Settings.setText(_translate("MainWindow", "Scan View Setting"))
        self.actionShow_Scan.setText(_translate("MainWindow", "Show Scan Tab"))
        self.actionShow_Log.setText(_translate("MainWindow", "Show Log"))
        self.actionDose_View_Settings.setText(_translate("MainWindow", "Dose View Settings"))

