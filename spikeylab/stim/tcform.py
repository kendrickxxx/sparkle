# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\tuning_curve.ui'
#
# Created: Wed Jun 18 16:50:03 2014
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

class Ui_TuningCurveEditor(object):
    def setupUi(self, TuningCurveEditor):
        TuningCurveEditor.setObjectName(_fromUtf8("TuningCurveEditor"))
        TuningCurveEditor.resize(599, 285)
        self.verticalLayout = QtGui.QVBoxLayout(TuningCurveEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.dbStopSpnbx = QtGui.QSpinBox(TuningCurveEditor)
        self.dbStopSpnbx.setMaximum(120)
        self.dbStopSpnbx.setProperty("value", 110)
        self.dbStopSpnbx.setObjectName(_fromUtf8("dbStopSpnbx"))
        self.gridLayout_2.addWidget(self.dbStopSpnbx, 2, 2, 1, 1)
        self.freqStopSpnbx = QtGui.QSpinBox(TuningCurveEditor)
        self.freqStopSpnbx.setMaximum(200)
        self.freqStopSpnbx.setProperty("value", 150)
        self.freqStopSpnbx.setObjectName(_fromUtf8("freqStopSpnbx"))
        self.gridLayout_2.addWidget(self.freqStopSpnbx, 1, 2, 1, 1)
        self.label_21 = QtGui.QLabel(TuningCurveEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_2.addWidget(self.label_21, 2, 4, 1, 1)
        self.funit_lbl_0 = QtGui.QLabel(TuningCurveEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.funit_lbl_0.sizePolicy().hasHeightForWidth())
        self.funit_lbl_0.setSizePolicy(sizePolicy)
        self.funit_lbl_0.setObjectName(_fromUtf8("funit_lbl_0"))
        self.gridLayout_2.addWidget(self.funit_lbl_0, 1, 4, 1, 1)
        self.freqStartSpnbx = QtGui.QSpinBox(TuningCurveEditor)
        self.freqStartSpnbx.setMaximum(200)
        self.freqStartSpnbx.setSingleStep(5)
        self.freqStartSpnbx.setProperty("value", 5)
        self.freqStartSpnbx.setObjectName(_fromUtf8("freqStartSpnbx"))
        self.gridLayout_2.addWidget(self.freqStartSpnbx, 1, 1, 1, 1)
        self.dbStartSpnbx = QtGui.QSpinBox(TuningCurveEditor)
        self.dbStartSpnbx.setMaximum(150)
        self.dbStartSpnbx.setSingleStep(5)
        self.dbStartSpnbx.setProperty("value", 0)
        self.dbStartSpnbx.setObjectName(_fromUtf8("dbStartSpnbx"))
        self.gridLayout_2.addWidget(self.dbStartSpnbx, 2, 1, 1, 1)
        self.label_25 = QtGui.QLabel(TuningCurveEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout_2.addWidget(self.label_25, 1, 0, 1, 1)
        self.label_26 = QtGui.QLabel(TuningCurveEditor)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout_2.addWidget(self.label_26, 0, 1, 1, 1)
        self.label_18 = QtGui.QLabel(TuningCurveEditor)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 2, 0, 1, 1)
        self.label_27 = QtGui.QLabel(TuningCurveEditor)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.gridLayout_2.addWidget(self.label_27, 0, 2, 1, 1)
        self.label_28 = QtGui.QLabel(TuningCurveEditor)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.gridLayout_2.addWidget(self.label_28, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(TuningCurveEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 5, 1, 1)
        self.dbStepSpnbx = SmartSpinBox(TuningCurveEditor)
        self.dbStepSpnbx.setObjectName(_fromUtf8("dbStepSpnbx"))
        self.gridLayout_2.addWidget(self.dbStepSpnbx, 2, 3, 1, 1)
        self.freqStepSpnbx = SmartSpinBox(TuningCurveEditor)
        self.freqStepSpnbx.setObjectName(_fromUtf8("freqStepSpnbx"))
        self.gridLayout_2.addWidget(self.freqStepSpnbx, 1, 3, 1, 1)
        self.freqNstepsLbl = QtGui.QLineEdit(TuningCurveEditor)
        self.freqNstepsLbl.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freqNstepsLbl.sizePolicy().hasHeightForWidth())
        self.freqNstepsLbl.setSizePolicy(sizePolicy)
        self.freqNstepsLbl.setMaximumSize(QtCore.QSize(50, 16777215))
        self.freqNstepsLbl.setInputMask(_fromUtf8(""))
        self.freqNstepsLbl.setFrame(False)
        self.freqNstepsLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.freqNstepsLbl.setObjectName(_fromUtf8("freqNstepsLbl"))
        self.gridLayout_2.addWidget(self.freqNstepsLbl, 1, 5, 1, 1)
        self.dbNstepsLbl = QtGui.QLineEdit(TuningCurveEditor)
        self.dbNstepsLbl.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbNstepsLbl.sizePolicy().hasHeightForWidth())
        self.dbNstepsLbl.setSizePolicy(sizePolicy)
        self.dbNstepsLbl.setMaximumSize(QtCore.QSize(50, 16777215))
        self.dbNstepsLbl.setFrame(False)
        self.dbNstepsLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dbNstepsLbl.setObjectName(_fromUtf8("dbNstepsLbl"))
        self.gridLayout_2.addWidget(self.dbNstepsLbl, 2, 5, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_14 = QtGui.QLabel(TuningCurveEditor)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_3.addWidget(self.label_14, 0, 3, 1, 1)
        self.label_22 = QtGui.QLabel(TuningCurveEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout_3.addWidget(self.label_22, 0, 0, 1, 1)
        self.tunit_lbl_4 = QtGui.QLabel(TuningCurveEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tunit_lbl_4.sizePolicy().hasHeightForWidth())
        self.tunit_lbl_4.setSizePolicy(sizePolicy)
        self.tunit_lbl_4.setObjectName(_fromUtf8("tunit_lbl_4"))
        self.gridLayout_3.addWidget(self.tunit_lbl_4, 0, 2, 1, 1)
        self.tunit_lbl_3 = QtGui.QLabel(TuningCurveEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tunit_lbl_3.sizePolicy().hasHeightForWidth())
        self.tunit_lbl_3.setSizePolicy(sizePolicy)
        self.tunit_lbl_3.setObjectName(_fromUtf8("tunit_lbl_3"))
        self.gridLayout_3.addWidget(self.tunit_lbl_3, 0, 5, 1, 1)
        self.nrepsSpnbx = QtGui.QSpinBox(TuningCurveEditor)
        self.nrepsSpnbx.setMinimum(1)
        self.nrepsSpnbx.setMaximum(100)
        self.nrepsSpnbx.setProperty("value", 5)
        self.nrepsSpnbx.setObjectName(_fromUtf8("nrepsSpnbx"))
        self.gridLayout_3.addWidget(self.nrepsSpnbx, 1, 4, 1, 1)
        self.label_31 = QtGui.QLabel(TuningCurveEditor)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.gridLayout_3.addWidget(self.label_31, 1, 3, 1, 1)
        self.durSpnbx = SmartSpinBox(TuningCurveEditor)
        self.durSpnbx.setMaximum(1000.0)
        self.durSpnbx.setObjectName(_fromUtf8("durSpnbx"))
        self.gridLayout_3.addWidget(self.durSpnbx, 0, 1, 1, 1)
        self.risefallSpnbx = SmartSpinBox(TuningCurveEditor)
        self.risefallSpnbx.setObjectName(_fromUtf8("risefallSpnbx"))
        self.gridLayout_3.addWidget(self.risefallSpnbx, 0, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.saveBtn = QtGui.QPushButton(TuningCurveEditor)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout.addWidget(self.saveBtn)
        self.okBtn = QtGui.QPushButton(TuningCurveEditor)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.horizontalLayout.addWidget(self.okBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TuningCurveEditor)
        QtCore.QObject.connect(self.okBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), TuningCurveEditor.close)
        QtCore.QObject.connect(self.nrepsSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.setStimReps)
        QtCore.QObject.connect(self.freqStartSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.submit)
        QtCore.QObject.connect(self.dbStartSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.submit)
        QtCore.QObject.connect(self.freqStopSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.submit)
        QtCore.QObject.connect(self.dbStopSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.submit)
        QtCore.QObject.connect(self.durSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.setStimDuration)
        QtCore.QObject.connect(self.risefallSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.setStimRisefall)
        QtCore.QObject.connect(self.saveBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), TuningCurveEditor.saveStimulus)
        QtCore.QObject.connect(self.freqStepSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.submit)
        QtCore.QObject.connect(self.dbStepSpnbx, QtCore.SIGNAL(_fromUtf8("editingFinished()")), TuningCurveEditor.submit)
        QtCore.QMetaObject.connectSlotsByName(TuningCurveEditor)

    def retranslateUi(self, TuningCurveEditor):
        TuningCurveEditor.setWindowTitle(_translate("TuningCurveEditor", "Form", None))
        self.label_21.setText(_translate("TuningCurveEditor", "dB SPL", None))
        self.funit_lbl_0.setText(_translate("TuningCurveEditor", "kHz", None))
        self.label_25.setText(_translate("TuningCurveEditor", "Frequency", None))
        self.label_26.setText(_translate("TuningCurveEditor", "Start", None))
        self.label_18.setText(_translate("TuningCurveEditor", "Intensity", None))
        self.label_27.setText(_translate("TuningCurveEditor", "Stop", None))
        self.label_28.setText(_translate("TuningCurveEditor", "Step", None))
        self.label_3.setText(_translate("TuningCurveEditor", "No. steps", None))
        self.freqNstepsLbl.setText(_translate("TuningCurveEditor", "-1", None))
        self.dbNstepsLbl.setText(_translate("TuningCurveEditor", "-1", None))
        self.label_14.setText(_translate("TuningCurveEditor", "Rise fall time", None))
        self.label_22.setText(_translate("TuningCurveEditor", "Duration", None))
        self.tunit_lbl_4.setText(_translate("TuningCurveEditor", "ms", None))
        self.tunit_lbl_3.setText(_translate("TuningCurveEditor", "ms", None))
        self.label_31.setText(_translate("TuningCurveEditor", "Reps", None))
        self.saveBtn.setText(_translate("TuningCurveEditor", "Save As...", None))
        self.okBtn.setText(_translate("TuningCurveEditor", "Ok", None))

from spikeylab.stim.smart_spinbox import SmartSpinBox
