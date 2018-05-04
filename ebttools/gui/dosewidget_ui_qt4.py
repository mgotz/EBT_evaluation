# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dosewidget_QtDesign.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_DoseWidget(object):
    def setupUi(self, DoseWidget):
        DoseWidget.setObjectName(_fromUtf8("DoseWidget"))
        DoseWidget.resize(937, 690)
        self.gridLayout = QtGui.QGridLayout(DoseWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(DoseWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget_2 = QtGui.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.imageLayout = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.imageLayout.setObjectName(_fromUtf8("imageLayout"))
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setToolTip(_fromUtf8(""))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.ViewTab = QtGui.QWidget()
        self.ViewTab.setObjectName(_fromUtf8("ViewTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.ViewTab)
        self.verticalLayout_2.setMargin(10)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.ViewTab)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.ViewTab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.doseMin = QtGui.QDoubleSpinBox(self.ViewTab)
        self.doseMin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doseMin.setDecimals(4)
        self.doseMin.setObjectName(_fromUtf8("doseMin"))
        self.horizontalLayout.addWidget(self.doseMin)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(self.ViewTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.doseMax = QtGui.QDoubleSpinBox(self.ViewTab)
        self.doseMax.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doseMax.setDecimals(4)
        self.doseMax.setObjectName(_fromUtf8("doseMax"))
        self.horizontalLayout.addWidget(self.doseMax)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.bestLimits = QtGui.QPushButton(self.ViewTab)
        self.bestLimits.setObjectName(_fromUtf8("bestLimits"))
        self.verticalLayout_2.addWidget(self.bestLimits)
        self.line = QtGui.QFrame(self.ViewTab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, 0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.showIsoLines = QtGui.QCheckBox(self.ViewTab)
        self.showIsoLines.setObjectName(_fromUtf8("showIsoLines"))
        self.horizontalLayout_6.addWidget(self.showIsoLines)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_15 = QtGui.QLabel(self.ViewTab)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_7.addWidget(self.label_15)
        self.nominalDose = QtGui.QDoubleSpinBox(self.ViewTab)
        self.nominalDose.setEnabled(False)
        self.nominalDose.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nominalDose.setDecimals(4)
        self.nominalDose.setObjectName(_fromUtf8("nominalDose"))
        self.horizontalLayout_7.addWidget(self.nominalDose)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.isoListField = QtGui.QTextEdit(self.ViewTab)
        self.isoListField.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.isoListField.sizePolicy().hasHeightForWidth())
        self.isoListField.setSizePolicy(sizePolicy)
        self.isoListField.setObjectName(_fromUtf8("isoListField"))
        self.horizontalLayout_2.addWidget(self.isoListField)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.line_3 = QtGui.QFrame(self.ViewTab)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout_2.addWidget(self.line_3)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.smooth = QtGui.QCheckBox(self.ViewTab)
        self.smooth.setObjectName(_fromUtf8("smooth"))
        self.horizontalLayout_12.addWidget(self.smooth)
        self.smoothFunction = QtGui.QComboBox(self.ViewTab)
        self.smoothFunction.setObjectName(_fromUtf8("smoothFunction"))
        self.horizontalLayout_12.addWidget(self.smoothFunction)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.gaussSettingsLayout = QtGui.QHBoxLayout()
        self.gaussSettingsLayout.setContentsMargins(-1, 0, -1, -1)
        self.gaussSettingsLayout.setObjectName(_fromUtf8("gaussSettingsLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gaussSettingsLayout.addItem(spacerItem4)
        self.label_23 = QtGui.QLabel(self.ViewTab)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gaussSettingsLayout.addWidget(self.label_23)
        self.smoothSigma = QtGui.QDoubleSpinBox(self.ViewTab)
        self.smoothSigma.setProperty("value", 1.0)
        self.smoothSigma.setObjectName(_fromUtf8("smoothSigma"))
        self.gaussSettingsLayout.addWidget(self.smoothSigma)
        self.verticalLayout_5.addLayout(self.gaussSettingsLayout)
        self.sgSettingsLayout = QtGui.QHBoxLayout()
        self.sgSettingsLayout.setContentsMargins(-1, 0, -1, -1)
        self.sgSettingsLayout.setObjectName(_fromUtf8("sgSettingsLayout"))
        spacerItem5 = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.sgSettingsLayout.addItem(spacerItem5)
        self.smoothLabel1 = QtGui.QLabel(self.ViewTab)
        self.smoothLabel1.setObjectName(_fromUtf8("smoothLabel1"))
        self.sgSettingsLayout.addWidget(self.smoothLabel1)
        self.smoothWindowSize = QtGui.QSpinBox(self.ViewTab)
        self.smoothWindowSize.setMinimum(3)
        self.smoothWindowSize.setMaximum(100)
        self.smoothWindowSize.setSingleStep(2)
        self.smoothWindowSize.setProperty("value", 3)
        self.smoothWindowSize.setProperty("toolTipDuration", -4)
        self.smoothWindowSize.setObjectName(_fromUtf8("smoothWindowSize"))
        self.sgSettingsLayout.addWidget(self.smoothWindowSize)
        self.smoothLabel2 = QtGui.QLabel(self.ViewTab)
        self.smoothLabel2.setObjectName(_fromUtf8("smoothLabel2"))
        self.sgSettingsLayout.addWidget(self.smoothLabel2)
        self.smoothOrder = QtGui.QSpinBox(self.ViewTab)
        self.smoothOrder.setMinimum(0)
        self.smoothOrder.setMaximum(100)
        self.smoothOrder.setProperty("value", 2)
        self.smoothOrder.setObjectName(_fromUtf8("smoothOrder"))
        self.sgSettingsLayout.addWidget(self.smoothOrder)
        self.verticalLayout_5.addLayout(self.sgSettingsLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.line_6 = QtGui.QFrame(self.ViewTab)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.verticalLayout_2.addWidget(self.line_6)
        self.refreshButton = QtGui.QPushButton(self.ViewTab)
        self.refreshButton.setObjectName(_fromUtf8("refreshButton"))
        self.verticalLayout_2.addWidget(self.refreshButton)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.line_2 = QtGui.QFrame(self.ViewTab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.exportTxtButton = QtGui.QPushButton(self.ViewTab)
        self.exportTxtButton.setObjectName(_fromUtf8("exportTxtButton"))
        self.horizontalLayout_5.addWidget(self.exportTxtButton)
        self.exportNpButton = QtGui.QPushButton(self.ViewTab)
        self.exportNpButton.setObjectName(_fromUtf8("exportNpButton"))
        self.horizontalLayout_5.addWidget(self.exportNpButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.ViewTab, _fromUtf8(""))
        self.CalcTab = QtGui.QWidget()
        self.CalcTab.setObjectName(_fromUtf8("CalcTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.CalcTab)
        self.verticalLayout.setMargin(10)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_21 = QtGui.QLabel(self.CalcTab)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.verticalLayout.addWidget(self.label_21)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_9 = QtGui.QLabel(self.CalcTab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        spacerItem7 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.evalFunction = QtGui.QComboBox(self.CalcTab)
        self.evalFunction.setObjectName(_fromUtf8("evalFunction"))
        self.horizontalLayout_3.addWidget(self.evalFunction)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_10 = QtGui.QLabel(self.CalcTab)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout.addWidget(self.label_10)
        self.newInputGrid = QtGui.QGridLayout()
        self.newInputGrid.setContentsMargins(0, 0, -1, -1)
        self.newInputGrid.setObjectName(_fromUtf8("newInputGrid"))
        self.label_5 = QtGui.QLabel(self.CalcTab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.newInputGrid.addWidget(self.label_5, 1, 1, 1, 1)
        self.height = QtGui.QDoubleSpinBox(self.CalcTab)
        self.height.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.height.setDecimals(4)
        self.height.setSingleStep(0.01)
        self.height.setObjectName(_fromUtf8("height"))
        self.newInputGrid.addWidget(self.height, 1, 5, 1, 1)
        self.label_4 = QtGui.QLabel(self.CalcTab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.newInputGrid.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.CalcTab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.newInputGrid.addWidget(self.label_7, 1, 4, 1, 1)
        self.yCenter = QtGui.QDoubleSpinBox(self.CalcTab)
        self.yCenter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.yCenter.setDecimals(4)
        self.yCenter.setSingleStep(0.01)
        self.yCenter.setObjectName(_fromUtf8("yCenter"))
        self.newInputGrid.addWidget(self.yCenter, 0, 5, 1, 1)
        self.label_6 = QtGui.QLabel(self.CalcTab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.newInputGrid.addWidget(self.label_6, 0, 4, 1, 1)
        self.width = QtGui.QDoubleSpinBox(self.CalcTab)
        self.width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.width.setDecimals(4)
        self.width.setSingleStep(0.01)
        self.width.setObjectName(_fromUtf8("width"))
        self.newInputGrid.addWidget(self.width, 1, 2, 1, 1)
        self.xCenter = QtGui.QDoubleSpinBox(self.CalcTab)
        self.xCenter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xCenter.setDecimals(4)
        self.xCenter.setSingleStep(0.01)
        self.xCenter.setObjectName(_fromUtf8("xCenter"))
        self.newInputGrid.addWidget(self.xCenter, 0, 2, 1, 1)
        self.angle = QtGui.QDoubleSpinBox(self.CalcTab)
        self.angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.angle.setDecimals(4)
        self.angle.setMinimum(-360.0)
        self.angle.setMaximum(360.0)
        self.angle.setObjectName(_fromUtf8("angle"))
        self.newInputGrid.addWidget(self.angle, 2, 5, 1, 1)
        self.label_8 = QtGui.QLabel(self.CalcTab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.newInputGrid.addWidget(self.label_8, 2, 4, 1, 1)
        spacerItem9 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.newInputGrid.addItem(spacerItem9, 0, 3, 1, 1)
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.newInputGrid.addItem(spacerItem10, 0, 6, 1, 1)
        self.verticalLayout.addLayout(self.newInputGrid)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.alternateSpecToggle = QtGui.QCheckBox(self.CalcTab)
        self.alternateSpecToggle.setObjectName(_fromUtf8("alternateSpecToggle"))
        self.horizontalLayout_4.addWidget(self.alternateSpecToggle)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.oldInputGrid = QtGui.QGridLayout()
        self.oldInputGrid.setContentsMargins(-1, 10, -1, -1)
        self.oldInputGrid.setObjectName(_fromUtf8("oldInputGrid"))
        self.x0 = QtGui.QDoubleSpinBox(self.CalcTab)
        self.x0.setEnabled(False)
        self.x0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x0.setDecimals(4)
        self.x0.setSingleStep(0.01)
        self.x0.setObjectName(_fromUtf8("x0"))
        self.oldInputGrid.addWidget(self.x0, 0, 2, 1, 1)
        self.x1 = QtGui.QDoubleSpinBox(self.CalcTab)
        self.x1.setEnabled(False)
        self.x1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x1.setDecimals(4)
        self.x1.setSingleStep(0.01)
        self.x1.setObjectName(_fromUtf8("x1"))
        self.oldInputGrid.addWidget(self.x1, 1, 2, 1, 1)
        self.y1 = QtGui.QDoubleSpinBox(self.CalcTab)
        self.y1.setEnabled(False)
        self.y1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y1.setDecimals(4)
        self.y1.setSingleStep(0.01)
        self.y1.setObjectName(_fromUtf8("y1"))
        self.oldInputGrid.addWidget(self.y1, 1, 5, 1, 1)
        self.y0 = QtGui.QDoubleSpinBox(self.CalcTab)
        self.y0.setEnabled(False)
        self.y0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y0.setDecimals(4)
        self.y0.setSingleStep(0.01)
        self.y0.setObjectName(_fromUtf8("y0"))
        self.oldInputGrid.addWidget(self.y0, 0, 5, 1, 1)
        self.label_11 = QtGui.QLabel(self.CalcTab)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.oldInputGrid.addWidget(self.label_11, 0, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.CalcTab)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.oldInputGrid.addWidget(self.label_12, 1, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.CalcTab)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.oldInputGrid.addWidget(self.label_13, 0, 4, 1, 1)
        self.label_14 = QtGui.QLabel(self.CalcTab)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.oldInputGrid.addWidget(self.label_14, 1, 4, 1, 1)
        spacerItem11 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.oldInputGrid.addItem(spacerItem11, 0, 3, 1, 1)
        spacerItem12 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.oldInputGrid.addItem(spacerItem12, 0, 6, 1, 1)
        self.verticalLayout.addLayout(self.oldInputGrid)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.useAsCenter = QtGui.QCheckBox(self.CalcTab)
        self.useAsCenter.setObjectName(_fromUtf8("useAsCenter"))
        self.horizontalLayout_13.addWidget(self.useAsCenter)
        self.useAsMax = QtGui.QCheckBox(self.CalcTab)
        self.useAsMax.setObjectName(_fromUtf8("useAsMax"))
        self.horizontalLayout_13.addWidget(self.useAsMax)
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem13)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.calculateButton = QtGui.QPushButton(self.CalcTab)
        self.calculateButton.setObjectName(_fromUtf8("calculateButton"))
        self.horizontalLayout_11.addWidget(self.calculateButton)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.clearFitButton = QtGui.QPushButton(self.CalcTab)
        self.clearFitButton.setObjectName(_fromUtf8("clearFitButton"))
        self.verticalLayout.addWidget(self.clearFitButton)
        self.line_4 = QtGui.QFrame(self.CalcTab)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout.addWidget(self.line_4)
        self.label_16 = QtGui.QLabel(self.CalcTab)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout.addWidget(self.label_16)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_17 = QtGui.QLabel(self.CalcTab)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_8.addWidget(self.label_17)
        self.saveTablePath = QtGui.QLineEdit(self.CalcTab)
        self.saveTablePath.setObjectName(_fromUtf8("saveTablePath"))
        self.horizontalLayout_8.addWidget(self.saveTablePath)
        self.browseSaveTable = QtGui.QPushButton(self.CalcTab)
        self.browseSaveTable.setObjectName(_fromUtf8("browseSaveTable"))
        self.horizontalLayout_8.addWidget(self.browseSaveTable)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem14)
        self.label_18 = QtGui.QLabel(self.CalcTab)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_9.addWidget(self.label_18)
        self.filmNumber = QtGui.QLineEdit(self.CalcTab)
        self.filmNumber.setObjectName(_fromUtf8("filmNumber"))
        self.horizontalLayout_9.addWidget(self.filmNumber)
        self.saveCalculationData = QtGui.QPushButton(self.CalcTab)
        self.saveCalculationData.setObjectName(_fromUtf8("saveCalculationData"))
        self.horizontalLayout_9.addWidget(self.saveCalculationData)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        spacerItem15 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem15)
        self.tabWidget.addTab(self.CalcTab, _fromUtf8(""))
        self.ExtraTab = QtGui.QWidget()
        self.ExtraTab.setObjectName(_fromUtf8("ExtraTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.ExtraTab)
        self.verticalLayout_4.setMargin(10)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_22 = QtGui.QLabel(self.ExtraTab)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.verticalLayout_4.addWidget(self.label_22)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_19 = QtGui.QLabel(self.ExtraTab)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.horizontalLayout_10.addWidget(self.label_19)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.ExtraTab)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.horizontalLayout_10.addWidget(self.doubleSpinBox)
        self.label_20 = QtGui.QLabel(self.ExtraTab)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.horizontalLayout_10.addWidget(self.label_20)
        spacerItem16 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem16)
        self.depthDoseButton = QtGui.QPushButton(self.ExtraTab)
        self.depthDoseButton.setObjectName(_fromUtf8("depthDoseButton"))
        self.horizontalLayout_10.addWidget(self.depthDoseButton)
        spacerItem17 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem17)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.line_5 = QtGui.QFrame(self.ExtraTab)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.verticalLayout_4.addWidget(self.line_5)
        spacerItem18 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem18)
        self.tabWidget.addTab(self.ExtraTab, _fromUtf8(""))
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
        DoseWidget.setWindowTitle(_translate("DoseWidget", "Form", None))
        self.label.setText(_translate("DoseWidget", "dose scale limits:", None))
        self.label_2.setText(_translate("DoseWidget", "min", None))
        self.label_3.setText(_translate("DoseWidget", "max", None))
        self.bestLimits.setText(_translate("DoseWidget", "restore default limits", None))
        self.showIsoLines.setToolTip(_translate("DoseWidget", "Check to show iso dose lines, requires a referesh", None))
        self.showIsoLines.setText(_translate("DoseWidget", "show iso dose lines", None))
        self.label_15.setText(_translate("DoseWidget", "nominal dose", None))
        self.nominalDose.setToolTip(_translate("DoseWidget", "From this dose the percentages are calculated to draw the iso dose lines", None))
        self.isoListField.setHtml(_translate("DoseWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">80</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">60</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">40</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">20</span></p></body></html>", None))
        self.smooth.setText(_translate("DoseWidget", "smooth data with", None))
        self.label_23.setText(_translate("DoseWidget", "sigma", None))
        self.smoothSigma.setToolTip(_translate("DoseWidget", "Sigma of the gaussian smoothing in pixels", None))
        self.smoothLabel1.setText(_translate("DoseWidget", "window size", None))
        self.smoothWindowSize.setToolTip(_translate("DoseWidget", "Window size for the Savitzky-Golay filter. Larger window size results in strong smoothing, can only be odd.", None))
        self.smoothLabel2.setText(_translate("DoseWidget", "order", None))
        self.smoothOrder.setToolTip(_translate("DoseWidget", "Order of the polynomial fitted in the Savitzky-Golay filter, must be windowSize-1, smaller will smooth more strongly. Order of 0 should be equivalent to a moving average.", None))
        self.refreshButton.setText(_translate("DoseWidget", "refresh dose plot", None))
        self.exportTxtButton.setToolTip(_translate("DoseWidget", "export the dose distribution into a txt file to use elsewhere (seperator is tab)", None))
        self.exportTxtButton.setText(_translate("DoseWidget", "export as txt", None))
        self.exportNpButton.setToolTip(_translate("DoseWidget", "export the dose distribution into a npy file which can be loaded by numpy.load() in python (smaller than txt)", None))
        self.exportNpButton.setText(_translate("DoseWidget", "export as numpy", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ViewTab), _translate("DoseWidget", "View and Export", None))
        self.label_21.setText(_translate("DoseWidget", "analyze dose distribution:", None))
        self.label_9.setText(_translate("DoseWidget", "evalution method", None))
        self.evalFunction.setToolTip(_translate("DoseWidget", "select what to do and over what area", None))
        self.label_10.setText(_translate("DoseWidget", "region of interest for evaluation", None))
        self.label_5.setText(_translate("DoseWidget", "width", None))
        self.height.setToolTip(_translate("DoseWidget", "height (y-direction), not used for profile", None))
        self.label_4.setText(_translate("DoseWidget", "x-center", None))
        self.label_7.setText(_translate("DoseWidget", "height", None))
        self.yCenter.setToolTip(_translate("DoseWidget", "y coordinate of the center of the ROI", None))
        self.label_6.setText(_translate("DoseWidget", "y-center", None))
        self.width.setToolTip(_translate("DoseWidget", "width (x-direction) of ROI or length of profile", None))
        self.xCenter.setToolTip(_translate("DoseWidget", "x coordinate of the center of the ROI", None))
        self.angle.setToolTip(_translate("DoseWidget", "roation angle of ROI (counter clockwise)", None))
        self.label_8.setText(_translate("DoseWidget", "angle", None))
        self.alternateSpecToggle.setText(_translate("DoseWidget", "use alternative/old region specification", None))
        self.label_11.setText(_translate("DoseWidget", "x0", None))
        self.label_12.setText(_translate("DoseWidget", "x1", None))
        self.label_13.setText(_translate("DoseWidget", "y0", None))
        self.label_14.setText(_translate("DoseWidget", "y1", None))
        self.useAsCenter.setToolTip(_translate("DoseWidget", "Use calculation results as input for x-center and y-center of ROI. Works only with methods that calculate a center-like coordinate, e.g. 2D Gauss or Max.", None))
        self.useAsCenter.setText(_translate("DoseWidget", "use result as center", None))
        self.useAsMax.setToolTip(_translate("DoseWidget", "Use the calculation result as max for the dose limits in the visualization. Only applicable to methods that output a maxlike value, e.g. 2D Gauss or center of mass.", None))
        self.useAsMax.setText(_translate("DoseWidget", "use result as max", None))
        self.calculateButton.setText(_translate("DoseWidget", "calculate", None))
        self.clearFitButton.setToolTip(_translate("DoseWidget", "remove the contour plot and the center marker created by 2D fit from the dose plot", None))
        self.clearFitButton.setText(_translate("DoseWidget", "clear 2D fit", None))
        self.label_16.setText(_translate("DoseWidget", "save calculation results to file:", None))
        self.label_17.setText(_translate("DoseWidget", "save results to:", None))
        self.saveTablePath.setToolTip(_translate("DoseWidget", "Path to save the data to. Each save operation appends an new line.", None))
        self.browseSaveTable.setToolTip(_translate("DoseWidget", "browse for the file instead of typing the path", None))
        self.browseSaveTable.setText(_translate("DoseWidget", "browse", None))
        self.label_18.setText(_translate("DoseWidget", "film no.", None))
        self.filmNumber.setToolTip(_translate("DoseWidget", "Give the number of the film. This is written as the first column to the save file.", None))
        self.saveCalculationData.setToolTip(_translate("DoseWidget", "Calculate and save the results of the calculation along with the data settings to reproduce it  to a new line in the save file.", None))
        self.saveCalculationData.setText(_translate("DoseWidget", "save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CalcTab), _translate("DoseWidget", "Calculate", None))
        self.label_22.setText(_translate("DoseWidget", "calculate the depth dose", None))
        self.label_19.setText(_translate("DoseWidget", "integration radius", None))
        self.doubleSpinBox.setToolTip(_translate("DoseWidget", "Lateral distance from the maximum that is considered in the integration. Should be large enough to include the entire beam at the distal edge.", None))
        self.label_20.setText(_translate("DoseWidget", "cm", None))
        self.depthDoseButton.setToolTip(_translate("DoseWidget", "Determine the maximum in y-direction for each slice in x-direction. Integrate over a circular area around the maximum und display this as the depth dose curve.", None))
        self.depthDoseButton.setText(_translate("DoseWidget", "show depth dose", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ExtraTab), _translate("DoseWidget", "Extras", None))

