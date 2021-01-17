# -*- coding: utf-8 -*-
import sys, os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication, QLabel
from PyQt5.uic import loadUi
from src.__init__ import get_root_path
import Scraping_Controller as sc

class ExtendedQLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, parent):
        super(ExtendedQLabel, self).__init__(parent)
        self.pos_x = None
        self.pos_y = None

    def mouseDoubleClickEvent(self, QMouseEvent):
        # Extract x- and y-positions of mouse double click
        self.pos_x = QMouseEvent.x()
        self.pos_y = QMouseEvent.y()

class ResizableQDialog(QDialog):
    resized = pyqtSignal()

    def __init__(self):
        super(ResizableQDialog, self).__init__()

    def resizeEvent(self, event):
        # Emit signal when resized (to connect to the function which resizes the widgets)
        self.resized.emit()

class ScrapingGUI(ResizableQDialog):
    def __init__(self):
        # The "super" function initialises the child class using the initialisation of the parent class,
        super(ScrapingGUI, self).__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)
        # Loads the UI
        loadUi(get_root_path() + 'src\\resources\\scraping.ui', self)
        
        # Basic button settings
        self.configLineEdit.setText(get_root_path() + 'Config\\job_ad_sites.csv')
        self.stopwordLineEdit.setText(get_root_path() + 'Config\\stopwords.txt')
        self.reportLineEdit.setText(get_root_path() + 'Report\\')
        
        # Browse for file
        self.configButton.clicked.connect(self.browse_config)
        self.stopwordButton.clicked.connect(self.browse_stopword)
        self.reportButton.clicked.connect(self.browse_report)
        
        self.startScrapeButton.clicked.connect(self.start)
        
    def start(self):
        pal = self.msgLabel.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("black"))
        self.msgLabel.setPalette(pal)
        
        self.startScrapeButton.setEnabled(False)
        if not all([self.configLineEdit.text(), self.reportLineEdit.text(), self.categoryLineEdit.text(), self.locationLineEdit.text()]):
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            self.msgLabel.setPalette(pal)
            self.msgLabel.setText('Please fill in all fields above (except stopword list path).')
            self.startScrapeButton.setEnabled(True)
            return
        
        sc.main(self.configLineEdit.text(), self.stopwordLineEdit.text(), self.reportLineEdit.text(), self.categoryLineEdit.text(), self.locationLineEdit.text(), self.msgLabel)
        
        # try:
        #     sc.main(self.configLineEdit.text(), self.stopwordLineEdit.text(), self.reportLineEdit.text(), self.categoryLineEdit.text(), self.locationLineEdit.text(), self.msgLabel)
        # except Exception as e:
        #     pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
        #     self.msgLabel.setPalette(pal)
        #     self.msgLabel.setText('{}'.format(repr(e)))
        # finally:
        #     self.startScrapeButton.setEnabled(True)
        
    def browse_config(self):
        self.browse(self.configLineEdit, "*.csv")
        
    def browse_stopword(self):
        self.browse(self.stopwordLineEdit, "*.txt")
        
    def browse_report(self):
        self.browse(self.reportLineEdit, "dir")
        
    def browse(self, lineEdit, fileType):
        if fileType == "dir":
            fname = QFileDialog.getExistingDirectory(self, "Browse Directory", get_root_path(), QFileDialog.ShowDirsOnly)
            fname += "\\"
        else:
            fname, filter = QFileDialog.getOpenFileName(self, "Browse Files", get_root_path(), "Files (" + fileType + ")")
        
        lineEdit.setText(os.path.normpath(fname))

class ScrapingApp(QApplication):
    def __init__(self, *args):
        super(ScrapingApp, self).__init__(*args)

        self.setQuitOnLastWindowClosed(True)

app = ScrapingApp(sys.argv)
# Create ScrapingGUI GUI object
window = ScrapingGUI()
# Set the title (G.13)
window.setWindowTitle("Scraping")
# Set the position and size of the dialog box (x-pos, y-pos, width, height)
# window.setGeometry(0, 100, 400, 200)
window.show()
# Execute the application
sys.exit(app.exec_())
