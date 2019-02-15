#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    PyQt4 conversion of Qt License Wizard Example

    A complex Wizard example where the path through the wizard depends
    on user choices.

    NOTES:
    =====

    Field Validation
    ----------------
    Fields are only validated if they are registered as mandatory
    (denoted by an asterisk after the name) even if they have
    been assigned a QRegExValidator.

    i.e.
        registerField("evaluate.email*", emailEdit) - validates
        registerField("evaluate.email", emailEdit) - no validation

    Button Positioning
    ------------------
    If you want to change the order in which the buttons appear
    you can set their layout; however, the layout ignores the visibility
    of the custom buttons so need to remove them from the layout to hide them.
    (see ConclusionPage._configWizBtns())

    Refactored
    ----------
    Refactored _showHelp() - extracted messages to _createHelpMsgs(),
    solely as an exercise in using Python dictionaries.

last modified: 2012-01-25 jg
ref:
    http://developer.qt.nokia.com/doc/qt-4.8/dialogs-licensewizard.html
'''
from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
                         QRadioButton, QVBoxLayout, QLineEdit, QGridLayout,
                         QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
                         QMessageBox)
from PyQt4.QtCore import (pyqtSlot, QRegExp)
import qrc_licwiz

class LicenseWizard(QWizard):
    NUM_PAGES = 5

    (PageIntro, PageEvaluate, PageRegister, PageDetails,
        PageConclusion) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(LicenseWizard, self).__init__(parent)

        self.setPage(self.PageIntro, IntroPage(self))
        self.setPage(self.PageEvaluate, EvaluatePage())
        self.setPage(self.PageRegister, RegisterPage())
        self.setPage(self.PageDetails, DetailsPage())
        self.setPage(self.PageConclusion, ConclusionPage())

        self.setStartId(self.PageIntro)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/logo.png"))

        # set up help messages
        self._lastHelpMsg = ''
        self._helpMsgs = self._createHelpMsgs()
        self.helpRequested.connect(self._showHelp)

        self.setWindowTitle(self.tr("License Wizard"))

    def _createHelpMsgs(self):
        msgs = {}
        msgs[self.PageIntro] = self.tr(
            "The decision you make here will affect which page you "
            "get to see next.")
        msgs[self.PageEvaluate] = self.tr(
            "Make sure to provide a valid email address, such as "
            "toni.buddenbrook@example.de.")
        msgs[self.PageRegister] = self.tr(
            "If you don't provide an upgrade key, you will be "
            "asked to fill in your details.")
        msgs[self.PageDetails] = self.tr(
            "Make sure to provide a valid email address, such as "
            "thomas.gradgrind@example.co.uk.")
        msgs[self.PageConclusion] = self.tr(
            "You must accept the terms and conditions of the "
            "license to proceed.")
        msgs[self.NUM_PAGES + 1] = self.tr("Sorry, I already gave what help I could. "
                          "\nMaybe you should try asking a human?")
        return msgs

    @pyqtSlot()
    def _showHelp(self):
        # get the help message for the current page
        msg = self._helpMsgs[self.currentId()]

        # if same as last message, display alternate message
        if msg == self._lastHelpMsg:
            msg = self._helpMsgs[self.NUM_PAGES + 1]

        QMessageBox.information(self,
                                self.tr("License Wizard Help"),
                                msg)
        self._lastHelpMsg = msg

class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr("Introduction"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))
        topLabel = QLabel(self.tr("This Wizard will help you register your copy of "
                                  "Super Product One™ or start "
                                  "evaluating the product."))
        topLabel.setWordWrap(True)

        regRBtn = QRadioButton(self.tr("&Register your copy"))
        self.evalRBtn = QRadioButton(self.tr("&Evaluate the product for 30 days"))
        regRBtn.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(regRBtn)
        layout.addWidget(self.evalRBtn)
        self.setLayout(layout)

    def nextId(self):
        if self.evalRBtn.isChecked():
            return LicenseWizard.PageEvaluate
        else:
            return LicenseWizard.PageRegister

class EvaluatePage(QWizardPage):
    def __init__(self, parent=None):
        super(EvaluatePage, self).__init__(parent)

        self.setTitle(self.tr("Evaluate Super Product One™"))
        self.setSubTitle(self.tr("Please fill both fields. \nMake sure to provide "
                                 "a valid email address (e.g. john.smith@example.com)"))
        nameLabel = QLabel("Name: ")
        nameEdit = QLineEdit()
        nameLabel.setBuddy(nameEdit)

        emailLabel = QLabel(self.tr("&Email address: "))
        emailEdit = QLineEdit()
        emailEdit.setValidator(QRegExpValidator(
                QRegExp(".*@.*"), self))
        emailLabel.setBuddy(emailEdit)

        self.registerField("evaluate.name*", nameEdit)
        self.registerField("evaluate.email*", emailEdit)

        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(nameEdit, 0, 1)
        grid.addWidget(emailLabel, 1, 0)
        grid.addWidget(emailEdit, 1, 1)
        self.setLayout(grid)

    def nextId(self):
        return LicenseWizard.PageConclusion

class RegisterPage(QWizardPage):
    def __init__(self, parent=None):
        super(RegisterPage, self).__init__(parent)

        self.setTitle(self.tr("Register Your Copy of Super Product One™"))
        self.setSubTitle(self.tr("If you have an upgrade key, please fill in "
                                 "the appropriate field."))
        nameLabel = QLabel(self.tr("N&ame"))
        nameEdit = QLineEdit()
        nameLabel.setBuddy(nameEdit)

        upgradeKeyLabel = QLabel(self.tr("&Upgrade key"))
        self.upgradeKeyEdit = QLineEdit()
        upgradeKeyLabel.setBuddy(self.upgradeKeyEdit)

        self.registerField("register.name*", nameEdit)
        self.registerField("register.upgradeKey", self.upgradeKeyEdit)

        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(nameEdit, 0, 1)
        grid.addWidget(upgradeKeyLabel, 1, 0)
        grid.addWidget(self.upgradeKeyEdit, 1, 1)

        self.setLayout(grid)

    def nextId(self):
        if len(self.upgradeKeyEdit.text()) > 0 :
            return LicenseWizard.PageConclusion
        else:
            return LicenseWizard.PageDetails


class DetailsPage(QWizardPage):
    def __init__(self, parent=None):
        super(DetailsPage, self).__init__(parent)

        self.setTitle(self.tr("Fill in Your Details"))
        self.setSubTitle(self.tr("Please fill all three fields. /n"
                                 "Make sure to provide a valid "
                                 "email address (e.g., tanaka.aya@example.com)."))
        coLabel = QLabel(self.tr("&Company name: "))
        coEdit = QLineEdit()
        coLabel.setBuddy(coEdit)

        emailLabel = QLabel(self.tr("&Email address: "))
        emailEdit = QLineEdit()
        emailEdit.setValidator(QRegExpValidator(QRegExp(".*@.*"), self))
        emailLabel.setBuddy(emailEdit)

        postLabel = QLabel(self.tr("&Postal address: "))
        postEdit = QLineEdit()
        postLabel.setBuddy(postEdit)

        self.registerField("details.company*", coEdit)
        self.registerField("details.email*", emailEdit)
        self.registerField("details.postal*", postEdit)

        grid = QGridLayout()
        grid.addWidget(coLabel, 0, 0)
        grid.addWidget(coEdit, 0, 1)
        grid.addWidget(emailLabel, 1, 0)
        grid.addWidget(emailEdit, 1, 1)
        grid.addWidget(postLabel, 2, 0)
        grid.addWidget(postEdit, 2, 1)
        self.setLayout(grid)

    def nextId(self):
        return LicenseWizard.PageConclusion

class ConclusionPage(QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle(self.tr("Complete Your Registration"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark.png"))

        self.bottomLabel = QLabel()
        self.bottomLabel.setWordWrap(True)

        agreeBox = QCheckBox(self.tr("I agree to the terms of the license."))

        self.registerField("conclusion.agree*", agreeBox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.bottomLabel)
        vbox.addWidget(agreeBox)
        self.setLayout(vbox)

    def nextId(self):
        return -1

    def initializePage(self):
        licenseText = ''

        if self.wizard().hasVisitedPage(LicenseWizard.PageEvaluate):
            licenseText = self.tr("Evaluation License Agreement: "
                          "You can use this software for 30 days and make one "
                          "backup, but you are not allowed to distribute it.")
        elif self.wizard().hasVisitedPage(LicenseWizard.PageDetails):
            licenseText = self.tr("First-Time License Agreement: "
                          "You can use this software subject to the license "
                          "you will receive by email.")
        else:
            licenseText = self.tr("Upgrade License Agreement: "
                          "This software is licensed under the terms of your "
                          "current license.")

        self.bottomLabel.setText(licenseText)

    def setVisible(self, visible):
        # only show the 'Print' button on the last page
        QWizardPage.setVisible(self, visible)

        if visible:
            self.wizard().setButtonText(QWizard.CustomButton1, self.tr("&Print"))
            self.wizard().setOption(QWizard.HaveCustomButton1, True)
            self.wizard().customButtonClicked.connect(self._printButtonClicked)
            self._configWizBtns(True)
        else:
            # only disconnect if button has been assigned and connected
            btn = self.wizard().button(QWizard.CustomButton1)
            if len(btn.text()) > 0:
                self.wizard().customButtonClicked.disconnect(self._printButtonClicked)

            self.wizard().setOption(QWizard.HaveCustomButton1, False)
            self._configWizBtns(False)

    def _configWizBtns(self, state):
        # position the Print button (CustomButton1) before the Finish button
        if state:
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.CustomButton1, QWizard.FinishButton,
                       QWizard.CancelButton, QWizard.HelpButton]
            self.wizard().setButtonLayout(btnList)
        else:
            # remove it if it's not visible
            btnList = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton,
                       QWizard.FinishButton,
                       QWizard.CancelButton, QWizard.HelpButton]
            self.wizard().setButtonLayout(btnList)

    @pyqtSlot()
    def _printButtonClicked(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_():
            QMessageBox.warning(self,
                                self.tr("Print License"),
                                self.tr("As an environment friendly measure, the "
                                        "license text will not actually be printed."))


# main ========================================================================
def main():
    import sys

    app = QApplication(sys.argv)
    wiz = LicenseWizard()
    wiz.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
