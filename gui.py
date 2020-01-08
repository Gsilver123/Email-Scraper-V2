from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLineEdit, QFileDialog, QPushButton, QWidget, QMessageBox, QVBoxLayout, \
    QDialog, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
import GoogleSearcher
import os.path
from os import path
import sys


class AppGui(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Q-Tips lil friend'
        self.left = 500
        self.top = 250
        self.width = 650
        self.height = 650
        self.fileLocation = ''
        self.fileName = ''
        self.searchList = []
        self.window()

    def window(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        font = QFont("Times", 14)

        self.placeTextBox(20, 70, 300, 30, "Input location you want to search:", font)
        self.locationEditText = self.placeQLineEdit(20, 100, 250, 30, font)

        self.placeTextBox(20, 170, 200, 30, "Add to search list", font)
        self.searchListEditText = self.placeQLineEdit(20, 200, 250, 30, font)
        self.placeButton(280, 200, 'Add', 'Add to the list with this button', font, self.onAddToSearchListClicked)
        self.placeButton(360, 200, 'Remove', 'Remove entries with this button', font, self.onRemoveToSearchListClicked)

        self.placeTextBox(20, 270, 200, 30, "Output file location:", font)
        self.outputFileLocationEditText = self.placeQLineEdit(20, 300, 475, 30, font)

        self.placeTextBox(20, 375, 200, 30, 'Enter file name:', font)
        self.outputFileNameEditText = self.placeQLineEdit(20, 405, 250, 30, font)

        self.placeButton(510, 300, 'File Search', 'Click here to find a file', font, self.onFileSearchClicked)

        self.checkBox = QCheckBox(self)
        self.checkBox.setText('Check to scape emails, else scrape phone numbers')
        self.checkBox.setFont(font)
        self.checkBox.setChecked(False)
        self.checkBox.move(20, 480)

        self.placeButton(20, 550, 'Meow (Go)', 'Click this. Meow', font, self.onGoClicked)

        self.show()

    def placeTextBox(self, xpos, ypos, width, height, text, font):
        label = QtWidgets.QLabel(self)
        label.setText(text)
        label.move(xpos, ypos)
        label.resize(width, height)
        label.setFont(font)

    def placeQLineEdit(self, xpos, ypos, width, height, font):
        qLineEdit = QLineEdit(self)
        qLineEdit.move(xpos, ypos)
        qLineEdit.resize(width, height)
        qLineEdit.setFont(font)

        return qLineEdit

    def placeButton(self, xpos, ypos, buttonText, toolTip, font, callback):
        outFileSearchButton = QPushButton(buttonText, self)
        outFileSearchButton.setToolTip(toolTip)
        outFileSearchButton.move(xpos, ypos)
        outFileSearchButton.setFont(font)
        outFileSearchButton.clicked.connect(callback)

    @pyqtSlot()
    def onAddToSearchListClicked(self):
        if self.searchListEditText.text() not in self.searchList:
            self.searchList.append(self.searchListEditText.text())
            self.searchListEditText.setText('')

    @pyqtSlot()
    def onRemoveToSearchListClicked(self):
        if len(self.searchList) > 0:
            removeSearchDialog = QVBoxLayout()
            dialogHeight = 0
            for i in self.searchList:
                button = QPushButton(str(i))
                button.clicked.connect(lambda: self.onRemoveItemFromDialog(i))
                removeSearchDialog.addWidget(button)
                dialogHeight += 100

            self.removeDialogBox = QDialog(self)
            self.removeDialogBox.resize(300, dialogHeight)
            self.removeDialogBox.setWindowTitle('Click to remove')
            self.removeDialogBox.setLayout(removeSearchDialog)
            self.removeDialogBox.exec_()

    @pyqtSlot()
    def onRemoveItemFromDialog(self, item):
        if item in self.searchList:
            self.searchList.remove(item)
            self.removeDialogBox.close()

    @pyqtSlot()
    def onFileSearchClicked(self):
        self.openFileNameOptions()

    @pyqtSlot()
    def onGoClicked(self):
        self.fileName = self.outputFileNameEditText.text()
        location = self.locationEditText.text()
        if len(location) <= 0 or len(self.fileName) <= 0 or len(self.searchList) <= 0 or len(self.fileLocation) <= 0:
            errorMessage = self.createMessageBox("Meow", "Please fill all fields before continuing, Thank you", "Error")
            errorMessage.exec_()
        else:
            file = self.fileLocation + '/' + self.fileName + '.csv'
            if path.exists(file):
                self.createMessageBox('File name already exists', 'Please choose another', 'Error')
                return
            is_email_scrape = self.checkBox.isChecked()
            self.close()
            GoogleSearcher.start_search(location, self.searchList, file, is_email_scrape)

    def openFileNameOptions(self):
        outFileDialogOptions = QFileDialog(self, "Choose File")
        outFileDialogOptions.setFileMode(QFileDialog.DirectoryOnly)
        outFileDialogOptions.exec_()
        self.fileLocation = outFileDialogOptions.selectedFiles()[0]
        self.outputFileLocationEditText.setText(self.fileLocation)

    def createMessageBox(self, text, infoText, title):
        messageBox = QMessageBox(self)
        messageBox.setText(text)
        messageBox.setInformativeText(infoText)
        messageBox.setWindowTitle(title)

        return messageBox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppGui()
    sys.exit(app.exec_())
