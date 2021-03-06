# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dosewidget_QtDesign.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DoseWidget(object):
    def setupUi(self, DoseWidget):
        DoseWidget.setObjectName("DoseWidget")
        DoseWidget.resize(937, 690)
        self.gridLayout = QtWidgets.QGridLayout(DoseWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(DoseWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.imageLayout = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.imageLayout.setContentsMargins(0, 0, 0, 0)
        self.imageLayout.setObjectName("imageLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        self.tabWidget.setToolTip("")
        self.tabWidget.setObjectName("tabWidget")
        self.ViewTab = QtWidgets.QWidget()
        self.ViewTab.setObjectName("ViewTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ViewTab)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.ViewTab)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.ViewTab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.doseMin = QtWidgets.QDoubleSpinBox(self.ViewTab)
        self.doseMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doseMin.setDecimals(4)
        self.doseMin.setObjectName("doseMin")
        self.horizontalLayout.addWidget(self.doseMin)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.ViewTab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.doseMax = QtWidgets.QDoubleSpinBox(self.ViewTab)
        self.doseMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doseMax.setDecimals(4)
        self.doseMax.setObjectName("doseMax")
        self.horizontalLayout.addWidget(self.doseMax)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.bestLimits = QtWidgets.QPushButton(self.ViewTab)
        self.bestLimits.setObjectName("bestLimits")
        self.verticalLayout_2.addWidget(self.bestLimits)
        self.line = QtWidgets.QFrame(self.ViewTab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.showIsoLines = QtWidgets.QCheckBox(self.ViewTab)
        self.showIsoLines.setObjectName("showIsoLines")
        self.horizontalLayout_6.addWidget(self.showIsoLines)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_15 = QtWidgets.QLabel(self.ViewTab)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_7.addWidget(self.label_15)
        self.nominalDose = QtWidgets.QDoubleSpinBox(self.ViewTab)
        self.nominalDose.setEnabled(False)
        self.nominalDose.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nominalDose.setDecimals(4)
        self.nominalDose.setObjectName("nominalDose")
        self.horizontalLayout_7.addWidget(self.nominalDose)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.isoListField = QtWidgets.QTextEdit(self.ViewTab)
        self.isoListField.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.isoListField.sizePolicy().hasHeightForWidth())
        self.isoListField.setSizePolicy(sizePolicy)
        self.isoListField.setObjectName("isoListField")
        self.horizontalLayout_2.addWidget(self.isoListField)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.line_3 = QtWidgets.QFrame(self.ViewTab)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.smooth = QtWidgets.QCheckBox(self.ViewTab)
        self.smooth.setObjectName("smooth")
        self.horizontalLayout_12.addWidget(self.smooth)
        self.smoothFunction = QtWidgets.QComboBox(self.ViewTab)
        self.smoothFunction.setObjectName("smoothFunction")
        self.horizontalLayout_12.addWidget(self.smoothFunction)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.gaussSettingsLayout = QtWidgets.QHBoxLayout()
        self.gaussSettingsLayout.setContentsMargins(-1, 0, -1, -1)
        self.gaussSettingsLayout.setObjectName("gaussSettingsLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gaussSettingsLayout.addItem(spacerItem4)
        self.label_23 = QtWidgets.QLabel(self.ViewTab)
        self.label_23.setObjectName("label_23")
        self.gaussSettingsLayout.addWidget(self.label_23)
        self.smoothSigma = QtWidgets.QDoubleSpinBox(self.ViewTab)
        self.smoothSigma.setProperty("value", 1.0)
        self.smoothSigma.setObjectName("smoothSigma")
        self.gaussSettingsLayout.addWidget(self.smoothSigma)
        self.verticalLayout_5.addLayout(self.gaussSettingsLayout)
        self.sgSettingsLayout = QtWidgets.QHBoxLayout()
        self.sgSettingsLayout.setContentsMargins(-1, 0, -1, -1)
        self.sgSettingsLayout.setObjectName("sgSettingsLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.sgSettingsLayout.addItem(spacerItem5)
        self.smoothLabel1 = QtWidgets.QLabel(self.ViewTab)
        self.smoothLabel1.setObjectName("smoothLabel1")
        self.sgSettingsLayout.addWidget(self.smoothLabel1)
        self.smoothWindowSize = QtWidgets.QSpinBox(self.ViewTab)
        self.smoothWindowSize.setMinimum(3)
        self.smoothWindowSize.setMaximum(100)
        self.smoothWindowSize.setSingleStep(2)
        self.smoothWindowSize.setProperty("value", 3)
        self.smoothWindowSize.setProperty("toolTipDuration", -4)
        self.smoothWindowSize.setObjectName("smoothWindowSize")
        self.sgSettingsLayout.addWidget(self.smoothWindowSize)
        self.smoothLabel2 = QtWidgets.QLabel(self.ViewTab)
        self.smoothLabel2.setObjectName("smoothLabel2")
        self.sgSettingsLayout.addWidget(self.smoothLabel2)
        self.smoothOrder = QtWidgets.QSpinBox(self.ViewTab)
        self.smoothOrder.setMinimum(0)
        self.smoothOrder.setMaximum(100)
        self.smoothOrder.setProperty("value", 2)
        self.smoothOrder.setObjectName("smoothOrder")
        self.sgSettingsLayout.addWidget(self.smoothOrder)
        self.verticalLayout_5.addLayout(self.sgSettingsLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.line_6 = QtWidgets.QFrame(self.ViewTab)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_2.addWidget(self.line_6)
        self.refreshButton = QtWidgets.QPushButton(self.ViewTab)
        self.refreshButton.setObjectName("refreshButton")
        self.verticalLayout_2.addWidget(self.refreshButton)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.line_2 = QtWidgets.QFrame(self.ViewTab)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.exportTxtButton = QtWidgets.QPushButton(self.ViewTab)
        self.exportTxtButton.setObjectName("exportTxtButton")
        self.horizontalLayout_5.addWidget(self.exportTxtButton)
        self.exportNpButton = QtWidgets.QPushButton(self.ViewTab)
        self.exportNpButton.setObjectName("exportNpButton")
        self.horizontalLayout_5.addWidget(self.exportNpButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.ViewTab, "")
        self.CalcTab = QtWidgets.QWidget()
        self.CalcTab.setObjectName("CalcTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.CalcTab)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_21 = QtWidgets.QLabel(self.CalcTab)
        self.label_21.setObjectName("label_21")
        self.verticalLayout.addWidget(self.label_21)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.CalcTab)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.evalFunction = QtWidgets.QComboBox(self.CalcTab)
        self.evalFunction.setObjectName("evalFunction")
        self.horizontalLayout_3.addWidget(self.evalFunction)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_10 = QtWidgets.QLabel(self.CalcTab)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.newInputGrid = QtWidgets.QGridLayout()
        self.newInputGrid.setContentsMargins(0, 0, -1, -1)
        self.newInputGrid.setObjectName("newInputGrid")
        self.label_5 = QtWidgets.QLabel(self.CalcTab)
        self.label_5.setObjectName("label_5")
        self.newInputGrid.addWidget(self.label_5, 1, 1, 1, 1)
        self.height = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.height.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.height.setDecimals(4)
        self.height.setSingleStep(0.01)
        self.height.setObjectName("height")
        self.newInputGrid.addWidget(self.height, 1, 5, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.CalcTab)
        self.label_4.setObjectName("label_4")
        self.newInputGrid.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.CalcTab)
        self.label_7.setObjectName("label_7")
        self.newInputGrid.addWidget(self.label_7, 1, 4, 1, 1)
        self.yCenter = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.yCenter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.yCenter.setDecimals(4)
        self.yCenter.setSingleStep(0.01)
        self.yCenter.setObjectName("yCenter")
        self.newInputGrid.addWidget(self.yCenter, 0, 5, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.CalcTab)
        self.label_6.setObjectName("label_6")
        self.newInputGrid.addWidget(self.label_6, 0, 4, 1, 1)
        self.width = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.width.setDecimals(4)
        self.width.setSingleStep(0.01)
        self.width.setObjectName("width")
        self.newInputGrid.addWidget(self.width, 1, 2, 1, 1)
        self.xCenter = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.xCenter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xCenter.setDecimals(4)
        self.xCenter.setSingleStep(0.01)
        self.xCenter.setObjectName("xCenter")
        self.newInputGrid.addWidget(self.xCenter, 0, 2, 1, 1)
        self.angle = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.angle.setDecimals(4)
        self.angle.setMinimum(-360.0)
        self.angle.setMaximum(360.0)
        self.angle.setObjectName("angle")
        self.newInputGrid.addWidget(self.angle, 2, 5, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.CalcTab)
        self.label_8.setObjectName("label_8")
        self.newInputGrid.addWidget(self.label_8, 2, 4, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.newInputGrid.addItem(spacerItem9, 0, 3, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.newInputGrid.addItem(spacerItem10, 0, 6, 1, 1)
        self.verticalLayout.addLayout(self.newInputGrid)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.alternateSpecToggle = QtWidgets.QCheckBox(self.CalcTab)
        self.alternateSpecToggle.setObjectName("alternateSpecToggle")
        self.horizontalLayout_4.addWidget(self.alternateSpecToggle)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.oldInputGrid = QtWidgets.QGridLayout()
        self.oldInputGrid.setContentsMargins(-1, 10, -1, -1)
        self.oldInputGrid.setObjectName("oldInputGrid")
        self.x0 = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.x0.setEnabled(False)
        self.x0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x0.setDecimals(4)
        self.x0.setSingleStep(0.01)
        self.x0.setObjectName("x0")
        self.oldInputGrid.addWidget(self.x0, 0, 2, 1, 1)
        self.x1 = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.x1.setEnabled(False)
        self.x1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x1.setDecimals(4)
        self.x1.setSingleStep(0.01)
        self.x1.setObjectName("x1")
        self.oldInputGrid.addWidget(self.x1, 1, 2, 1, 1)
        self.y1 = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.y1.setEnabled(False)
        self.y1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y1.setDecimals(4)
        self.y1.setSingleStep(0.01)
        self.y1.setObjectName("y1")
        self.oldInputGrid.addWidget(self.y1, 1, 5, 1, 1)
        self.y0 = QtWidgets.QDoubleSpinBox(self.CalcTab)
        self.y0.setEnabled(False)
        self.y0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y0.setDecimals(4)
        self.y0.setSingleStep(0.01)
        self.y0.setObjectName("y0")
        self.oldInputGrid.addWidget(self.y0, 0, 5, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.CalcTab)
        self.label_11.setObjectName("label_11")
        self.oldInputGrid.addWidget(self.label_11, 0, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.CalcTab)
        self.label_12.setObjectName("label_12")
        self.oldInputGrid.addWidget(self.label_12, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.CalcTab)
        self.label_13.setObjectName("label_13")
        self.oldInputGrid.addWidget(self.label_13, 0, 4, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.CalcTab)
        self.label_14.setObjectName("label_14")
        self.oldInputGrid.addWidget(self.label_14, 1, 4, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.oldInputGrid.addItem(spacerItem11, 0, 3, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.oldInputGrid.addItem(spacerItem12, 0, 6, 1, 1)
        self.verticalLayout.addLayout(self.oldInputGrid)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.useAsCenter = QtWidgets.QCheckBox(self.CalcTab)
        self.useAsCenter.setObjectName("useAsCenter")
        self.horizontalLayout_13.addWidget(self.useAsCenter)
        self.useAsMax = QtWidgets.QCheckBox(self.CalcTab)
        self.useAsMax.setObjectName("useAsMax")
        self.horizontalLayout_13.addWidget(self.useAsMax)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem13)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.calculateButton = QtWidgets.QPushButton(self.CalcTab)
        self.calculateButton.setObjectName("calculateButton")
        self.horizontalLayout_11.addWidget(self.calculateButton)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.clearFitButton = QtWidgets.QPushButton(self.CalcTab)
        self.clearFitButton.setObjectName("clearFitButton")
        self.verticalLayout.addWidget(self.clearFitButton)
        self.line_4 = QtWidgets.QFrame(self.CalcTab)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.label_16 = QtWidgets.QLabel(self.CalcTab)
        self.label_16.setObjectName("label_16")
        self.verticalLayout.addWidget(self.label_16)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_17 = QtWidgets.QLabel(self.CalcTab)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_8.addWidget(self.label_17)
        self.saveTablePath = QtWidgets.QLineEdit(self.CalcTab)
        self.saveTablePath.setObjectName("saveTablePath")
        self.horizontalLayout_8.addWidget(self.saveTablePath)
        self.browseSaveTable = QtWidgets.QPushButton(self.CalcTab)
        self.browseSaveTable.setObjectName("browseSaveTable")
        self.horizontalLayout_8.addWidget(self.browseSaveTable)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem14)
        self.label_18 = QtWidgets.QLabel(self.CalcTab)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_9.addWidget(self.label_18)
        self.filmNumber = QtWidgets.QLineEdit(self.CalcTab)
        self.filmNumber.setObjectName("filmNumber")
        self.horizontalLayout_9.addWidget(self.filmNumber)
        self.saveCalculationData = QtWidgets.QPushButton(self.CalcTab)
        self.saveCalculationData.setObjectName("saveCalculationData")
        self.horizontalLayout_9.addWidget(self.saveCalculationData)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem15)
        self.tabWidget.addTab(self.CalcTab, "")
        self.ExtraTab = QtWidgets.QWidget()
        self.ExtraTab.setObjectName("ExtraTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ExtraTab)
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_22 = QtWidgets.QLabel(self.ExtraTab)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_4.addWidget(self.label_22)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_19 = QtWidgets.QLabel(self.ExtraTab)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_10.addWidget(self.label_19)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.ExtraTab)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_10.addWidget(self.doubleSpinBox)
        self.label_20 = QtWidgets.QLabel(self.ExtraTab)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_10.addWidget(self.label_20)
        spacerItem16 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem16)
        self.depthDoseButton = QtWidgets.QPushButton(self.ExtraTab)
        self.depthDoseButton.setObjectName("depthDoseButton")
        self.horizontalLayout_10.addWidget(self.depthDoseButton)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem17)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.line_5 = QtWidgets.QFrame(self.ExtraTab)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_4.addWidget(self.line_5)
        spacerItem18 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem18)
        self.tabWidget.addTab(self.ExtraTab, "")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(DoseWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DoseWidget)
        DoseWidget.setTabOrder(self.tabWidget, self.doseMin)
        DoseWidget.setTabOrder(self.doseMin, self.doseMax)
        DoseWidget.setTabOrder(self.doseMax, self.bestLimits)
        DoseWidget.setTabOrder(self.bestLimits, self.showIsoLines)
        DoseWidget.setTabOrder(self.showIsoLines, self.nominalDose)
        DoseWidget.setTabOrder(self.nominalDose, self.isoListField)
        DoseWidget.setTabOrder(self.isoListField, self.refreshButton)
        DoseWidget.setTabOrder(self.refreshButton, self.exportTxtButton)
        DoseWidget.setTabOrder(self.exportTxtButton, self.exportNpButton)
        DoseWidget.setTabOrder(self.exportNpButton, self.evalFunction)
        DoseWidget.setTabOrder(self.evalFunction, self.xCenter)
        DoseWidget.setTabOrder(self.xCenter, self.yCenter)
        DoseWidget.setTabOrder(self.yCenter, self.width)
        DoseWidget.setTabOrder(self.width, self.height)
        DoseWidget.setTabOrder(self.height, self.angle)
        DoseWidget.setTabOrder(self.angle, self.alternateSpecToggle)
        DoseWidget.setTabOrder(self.alternateSpecToggle, self.x0)
        DoseWidget.setTabOrder(self.x0, self.y0)
        DoseWidget.setTabOrder(self.y0, self.x1)
        DoseWidget.setTabOrder(self.x1, self.y1)
        DoseWidget.setTabOrder(self.y1, self.calculateButton)
        DoseWidget.setTabOrder(self.calculateButton, self.clearFitButton)
        DoseWidget.setTabOrder(self.clearFitButton, self.saveTablePath)
        DoseWidget.setTabOrder(self.saveTablePath, self.browseSaveTable)
        DoseWidget.setTabOrder(self.browseSaveTable, self.filmNumber)
        DoseWidget.setTabOrder(self.filmNumber, self.saveCalculationData)
        DoseWidget.setTabOrder(self.saveCalculationData, self.doubleSpinBox)
        DoseWidget.setTabOrder(self.doubleSpinBox, self.depthDoseButton)

    def retranslateUi(self, DoseWidget):
        _translate = QtCore.QCoreApplication.translate
        DoseWidget.setWindowTitle(_translate("DoseWidget", "Form"))
        self.label.setText(_translate("DoseWidget", "dose scale limits:"))
        self.label_2.setText(_translate("DoseWidget", "min"))
        self.label_3.setText(_translate("DoseWidget", "max"))
        self.bestLimits.setText(_translate("DoseWidget", "restore default limits"))
        self.showIsoLines.setToolTip(_translate("DoseWidget", "Check to show iso dose lines, requires a referesh"))
        self.showIsoLines.setText(_translate("DoseWidget", "show iso dose lines"))
        self.label_15.setText(_translate("DoseWidget", "nominal dose"))
        self.nominalDose.setToolTip(_translate("DoseWidget", "From this dose the percentages are calculated to draw the iso dose lines"))
        self.isoListField.setHtml(_translate("DoseWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">80</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">60</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">40</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">20</span></p></body></html>"))
        self.smooth.setText(_translate("DoseWidget", "smooth data with"))
        self.label_23.setText(_translate("DoseWidget", "sigma"))
        self.smoothSigma.setToolTip(_translate("DoseWidget", "Sigma of the gaussian smoothing in pixels"))
        self.smoothLabel1.setText(_translate("DoseWidget", "window size"))
        self.smoothWindowSize.setToolTip(_translate("DoseWidget", "Window size for the Savitzky-Golay filter. Larger window size results in strong smoothing, can only be odd."))
        self.smoothLabel2.setText(_translate("DoseWidget", "order"))
        self.smoothOrder.setToolTip(_translate("DoseWidget", "Order of the polynomial fitted in the Savitzky-Golay filter, must be windowSize-1, smaller will smooth more strongly. Order of 0 should be equivalent to a moving average."))
        self.refreshButton.setText(_translate("DoseWidget", "refresh dose plot"))
        self.exportTxtButton.setToolTip(_translate("DoseWidget", "export the dose distribution into a txt file to use elsewhere (seperator is tab)"))
        self.exportTxtButton.setText(_translate("DoseWidget", "export as txt"))
        self.exportNpButton.setToolTip(_translate("DoseWidget", "export the dose distribution into a npy file which can be loaded by numpy.load() in python (smaller than txt)"))
        self.exportNpButton.setText(_translate("DoseWidget", "export as numpy"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ViewTab), _translate("DoseWidget", "View and Export"))
        self.label_21.setText(_translate("DoseWidget", "analyze dose distribution:"))
        self.label_9.setText(_translate("DoseWidget", "evalution method"))
        self.evalFunction.setToolTip(_translate("DoseWidget", "select what to do and over what area"))
        self.label_10.setText(_translate("DoseWidget", "region of interest for evaluation"))
        self.label_5.setText(_translate("DoseWidget", "width"))
        self.height.setToolTip(_translate("DoseWidget", "height (y-direction), not used for profile"))
        self.label_4.setText(_translate("DoseWidget", "x-center"))
        self.label_7.setText(_translate("DoseWidget", "height"))
        self.yCenter.setToolTip(_translate("DoseWidget", "y coordinate of the center of the ROI"))
        self.label_6.setText(_translate("DoseWidget", "y-center"))
        self.width.setToolTip(_translate("DoseWidget", "width (x-direction) of ROI or length of profile"))
        self.xCenter.setToolTip(_translate("DoseWidget", "x coordinate of the center of the ROI"))
        self.angle.setToolTip(_translate("DoseWidget", "roation angle of ROI (counter clockwise)"))
        self.label_8.setText(_translate("DoseWidget", "angle"))
        self.alternateSpecToggle.setText(_translate("DoseWidget", "use alternative/old region specification"))
        self.label_11.setText(_translate("DoseWidget", "x0"))
        self.label_12.setText(_translate("DoseWidget", "x1"))
        self.label_13.setText(_translate("DoseWidget", "y0"))
        self.label_14.setText(_translate("DoseWidget", "y1"))
        self.useAsCenter.setToolTip(_translate("DoseWidget", "Use calculation results as input for x-center and y-center of ROI. Works only with methods that calculate a center-like coordinate, e.g. 2D Gauss or Max."))
        self.useAsCenter.setText(_translate("DoseWidget", "use result as center"))
        self.useAsMax.setToolTip(_translate("DoseWidget", "Use the calculation result as max for the dose limits in the visualization. Only applicable to methods that output a maxlike value, e.g. 2D Gauss or center of mass."))
        self.useAsMax.setText(_translate("DoseWidget", "use result as max"))
        self.calculateButton.setText(_translate("DoseWidget", "calculate"))
        self.clearFitButton.setToolTip(_translate("DoseWidget", "remove the contour plot and the center marker created by 2D fit from the dose plot"))
        self.clearFitButton.setText(_translate("DoseWidget", "clear 2D fit"))
        self.label_16.setText(_translate("DoseWidget", "save calculation results to file:"))
        self.label_17.setText(_translate("DoseWidget", "save results to:"))
        self.saveTablePath.setToolTip(_translate("DoseWidget", "Path to save the data to. Each save operation appends an new line."))
        self.browseSaveTable.setToolTip(_translate("DoseWidget", "browse for the file instead of typing the path"))
        self.browseSaveTable.setText(_translate("DoseWidget", "browse"))
        self.label_18.setText(_translate("DoseWidget", "film no."))
        self.filmNumber.setToolTip(_translate("DoseWidget", "Give the number of the film. This is written as the first column to the save file."))
        self.saveCalculationData.setToolTip(_translate("DoseWidget", "Calculate and save the results of the calculation along with the data settings to reproduce it  to a new line in the save file."))
        self.saveCalculationData.setText(_translate("DoseWidget", "save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CalcTab), _translate("DoseWidget", "Calculate"))
        self.label_22.setText(_translate("DoseWidget", "calculate the depth dose"))
        self.label_19.setText(_translate("DoseWidget", "integration radius"))
        self.doubleSpinBox.setToolTip(_translate("DoseWidget", "Lateral distance from the maximum that is considered in the integration. Should be large enough to include the entire beam at the distal edge."))
        self.label_20.setText(_translate("DoseWidget", "cm"))
        self.depthDoseButton.setToolTip(_translate("DoseWidget", "Determine the maximum in y-direction for each slice in x-direction. Integrate over a circular area around the maximum und display this as the depth dose curve."))
        self.depthDoseButton.setText(_translate("DoseWidget", "show depth dose"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ExtraTab), _translate("DoseWidget", "Extras"))

