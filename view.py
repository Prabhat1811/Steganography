from PyQt6.QtWidgets import QApplication, QDialog, QStyleFactory, QComboBox, QDialogButtonBox, QFileDialog, QLabel, QTabWidget, QTextEdit, QWidget, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.uic.load_ui import loadUi
from PyQt6.uic.properties import QtWidgets
from Models import tools
from json import load
import sys

from controller import controller

#C:\Users\bipin\AppData\Local\Programs\Python\Python39\Lib\site-packages\qt6_applications\Qt\bin

__version__ = '2.3'
__author__ = 'Prabhat Bhartola'

UIPATH = r"UI/Encode2.3.ui"
ICONPATH = r"Content/Icon/newspaper.png"
APPNAME = r"SteganographyPy2.3"

def get_desc_from_code(errorCode):
    """
    Gives description from error code
    """
    with open("error_codes.json", "r") as ec:
        codes = load(ec)
        for code in codes["errorCodes"]:
            if code["code"] == errorCode:
                return code["error"]

# get_desc_from_code(1, 2)

class View(QWidget):
    """
    View class to implement the GUI
    """
    def __init__(self):
        super().__init__()
        loadUi(UIPATH, self)
        self.setWindowTitle(APPNAME)
        self.setWindowIcon(QIcon(ICONPATH))
        self.create_main_frame(800, 1200)
        self.assign_widgets()
        self.hide_label(self.label2)
        self.hide_label(self.label3)
        self.set_properties()
        self.init_var(0, "Image")

    def init_var(self, tab, file):
        """
        Initializes variables
        """
        self.tab = tab
        self.fType = file
        self.fName = ""
        self.msg = ""
        self.sign = ""
    
    def clear_all(self):
        self.textEdit1.clear()
        self.textEdit2.clear()
        self.textEdit3.clear()

    def create_main_frame(self, height : int, width : int) -> None:
        """
        Sets the main frame's boundary to fixed height and width
        """
        self.setFixedHeight(height)
        self.setFixedWidth(width)

    def assign_widgets(self) -> None:
        """
        Assigns widgets to their respective variables
        """
        self.folder = self.findChild(QTabWidget, "tabWidget")

        self.comboBox1 = self.findChild(QComboBox, "comboBox")
        self.dragDrop1 = self.findChild(QLabel, "label_9")
        self.pushButton1 = self.findChild(QPushButton, "pushButton_3")
        self.textEdit1 = self.findChild(QTextEdit, "textEdit")
        self.textEdit2 = self.findChild(QTextEdit, "textEdit_2")
        self.label1 = self.findChild(QLabel, "label_7")
        self.buttonBox1 = self.findChild(QDialogButtonBox, "buttonBox")
        self.label2 = self.findChild(QLabel, "label_11")
        self.label5 = self.findChild(QLabel, "label_14")

        self.comboBox2 = self.findChild(QComboBox, "comboBox_2")
        self.dragDrop2 = self.findChild(QLabel, "label_10")
        self.pushButton2 = self.findChild(QPushButton, "pushButton_4")
        self.textEdit3 = self.findChild(QTextEdit, "textEdit_3")
        self.buttonBox2 = self.findChild(QDialogButtonBox, "buttonBox_2")
        self.label3 = self.findChild(QLabel, "label_12")
        self.label6 = self.findChild(QLabel, "label_13")
    
    def show_label(self, label: object, text: str) -> None:
        label.setHidden(False)
        label.setText(text)

    def hide_label(self, label: object) -> None:
        label.setHidden(True)
        label.setText("")
    
    def set_properties(self) -> None:
        """
        Sets properties for widgets
        """
        self.textEdit1.setUndoRedoEnabled(False)
        self.textEdit2.setUndoRedoEnabled(False)
        self.textEdit3.setUndoRedoEnabled(False)
    
    def quit_app(self) -> None:
        """
        Quits the running application
        """
        print("EXIT")
        sys.exit()
    
    def get_value(self, button : object) -> None:
        """
        Returns the current value of the comboBox object
        """
        # print(button.currentText())
        self.fType = button.currentText()
    
    def browse_files(self, label1: object, label2: object) -> None:
        """
        Opens file explorer and Returns the name of selected file
        """
        fName = QFileDialog.getOpenFileName(self, "Choose File", r"\Documents")
        # print(fName[0])
        self.fName = fName[0]

        if self.fName != "":
            self.show_label(label1, tools.parse_name(self.fName))
            label2.setText("")

    def update_encode_label(self, error: bool, filename: str, directory: str):
        """
        Updates label with appropriate message
        """
        if error == False:
            txt = f"Success\nFile name - {filename}\nLocation - {directory}"
            self.label5.setText(txt)
        else:
            self.label5.setText(get_desc_from_code(error))
    
    def update_decode_label(self, error: bool, msg):
        if error == False:
            txt = f"Success\nMessage - {msg}"
            self.label6.setText(txt)
        else:
            self.label6.setText(get_desc_from_code(error))
            
    
    def clicked(self) -> None:
        print("clicked!")
    
    def set_file_name(self):
        """
        Sets label text to display the name of choosen file
        """
        pass
    
    def capture_text(self, textField1 : object, textField2 : object) -> dict:
        """
        Returns the inputed text from textField
        """
        if textField2 is None:
            # print({"signature": textField1.toPlainText()})
            self.sign = textField1.toPlainText()

        else:
            # print({"msg": textField1.toPlainText(), "signature": textField2.toPlainText()})
            self.msg = textField1.toPlainText()
            self.sign = textField2.toPlainText()
    
    def get_tab(self) -> int:
        """
        Returns tab index
        """
        # print(self.folder.currentIndex())
        self.tab = self.folder.currentIndex()

# Client code
def main() -> None:
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))
    view = View()
    view.show()
    controller(view)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()