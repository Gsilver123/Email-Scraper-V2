from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLineEdit, QFileDialog, QPushButton, QWidget, QMessageBox, QVBoxLayout, \
    QDialog, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
import GoogleSearcher
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
        self.file_location = ''
        self.file_name = ''
        self.search_list = []
        self.window()

    def window(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

        font = QFont("Times", 14)

        self.place_text_box(20, 70, 300, 30, "Input location you want to search:", font)
        self.location_edit_text = self.place_q_line_edit(20, 100, 250, 30, font)

        self.place_text_box(20, 170, 200, 30, "Add to search list", font)
        self.search_list_edit_text = self.place_q_line_edit(20, 200, 250, 30, font)
        self.place_button(280, 200, 'Add', 'Add to the list with this button', font, self.on_add_to_search_list_clicked)
        self.place_button(360, 200, 'Remove', 'Remove entries with this button', font, self.on_remove_to_search_list_clicked)

        self.place_text_box(20, 270, 200, 30, "Output file location:", font)
        self.output_file_location_edit_text = self.place_q_line_edit(20, 300, 475, 30, font)

        self.place_text_box(20, 375, 200, 30, 'Enter file name:', font)
        self.output_file_name_edit_text = self.place_q_line_edit(20, 405, 250, 30, font)

        self.place_button(510, 300, 'File Search', 'Click here to find a file', font, self.on_file_search_clicked)

        self.check_box = QCheckBox(self)
        self.check_box.setText('Check to scape emails, else scrape phone numbers')
        self.check_box.setFont(font)
        self.check_box.setChecked(False)
        self.check_box.move(20, 480)

        self.place_button(20, 550, 'Meow (Go)', 'Click this. Meow', font, self.on_go_clicked)

        self.show()

    def place_text_box(self, xpos, ypos, width, height, text, font):
        label = QtWidgets.QLabel(self)
        label.setText(text)
        label.move(xpos, ypos)
        label.resize(width, height)
        label.setFont(font)

    def place_q_line_edit(self, xpos, ypos, width, height, font):
        q_line_edit = QLineEdit(self)
        q_line_edit.move(xpos, ypos)
        q_line_edit.resize(width, height)
        q_line_edit.setFont(font)

        return q_line_edit

    def place_button(self, xpos, ypos, button_text, tool_tip, font, callback):
        out_file_search_button = QPushButton(button_text, self)
        out_file_search_button.setToolTip(tool_tip)
        out_file_search_button.move(xpos, ypos)
        out_file_search_button.setFont(font)
        out_file_search_button.clicked.connect(callback)

    @pyqtSlot()
    def on_add_to_search_list_clicked(self):
        if self.search_list_edit_text.text() not in self.search_list and len(self.search_list_edit_text.text()) > 0:
            self.search_list.append(self.search_list_edit_text.text())
            self.search_list_edit_text.setText('')

    @pyqtSlot()
    def on_remove_to_search_list_clicked(self):
        if len(self.search_list) > 0:
            remove_search_dialog = QVBoxLayout()
            dialog_height = 0
            font = QFont('Times', 12)
            check_box_list = []
            for i in self.search_list:
                remove_check_box = QCheckBox()
                remove_check_box.setText(str(i))
                remove_check_box.setFont(font)
                print(remove_check_box.text())
                check_box_list.append(remove_check_box)
                remove_search_dialog.addWidget(remove_check_box)
                dialog_height += 50

            button = QPushButton('Remove Selected')
            button.clicked.connect(lambda: self.on_remove_item_from_dialog(check_box_list))
            remove_search_dialog.addWidget(button)
            self.remove_dialog_box = QDialog(self)
            self.remove_dialog_box.resize(300, dialog_height)
            self.remove_dialog_box.setWindowTitle('Check to remove')
            self.remove_dialog_box.setLayout(remove_search_dialog)
            self.remove_dialog_box.exec_()

    @pyqtSlot()
    def on_remove_item_from_dialog(self, check_box_list):
        for i in check_box_list:
            if i.isChecked():
                self.search_list.remove(i.text())
        self.remove_dialog_box.close()

    @pyqtSlot()
    def on_file_search_clicked(self):
        self.open_file_name_options()

    @pyqtSlot()
    def on_go_clicked(self):
        self.file_name = self.output_file_name_edit_text.text()
        location = self.location_edit_text.text()
        if len(location) <= 0 or len(self.file_name) <= 0 or len(self.search_list) <= 0 or len(self.file_location) <= 0:
            error_message = self.create_message_box("Meow", "Please fill all fields before continuing, Thank you", "Error")
            error_message.exec_()
        else:
            file = self.file_location + '/' + self.file_name + '.csv'
            if path.exists(file):
                self.create_message_box('File name already exists', 'Please choose another', 'Error')
                return
            is_email_scrape = self.check_box.isChecked()
            self.close()
            GoogleSearcher.start_search(location, self.search_list, file, is_email_scrape)

    def open_file_name_options(self):
        out_file_dialog_options = QFileDialog(self, "Choose File")
        out_file_dialog_options.setFileMode(QFileDialog.DirectoryOnly)
        out_file_dialog_options.exec_()
        self.file_location = out_file_dialog_options.selectedFiles()[0]
        self.output_file_location_edit_text.setText(self.file_location)

    def create_message_box(self, text, info_text, title):
        message_box = QMessageBox(self)
        message_box.setText(text)
        message_box.setInformativeText(info_text)
        message_box.setWindowTitle(title)

        return message_box


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppGui()
    sys.exit(app.exec_())
