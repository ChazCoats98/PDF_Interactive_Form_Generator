from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets import FileUploadButton

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Interactive Form Generator')
        self.resize(500, 600)
        
        self.mainWidget = QWidget(self)
        self.mainLayout = QGridLayout()
        
        tagline = QLabel('Interactive Form Generator')
        self.mainLayout.addWidget(tagline, 2, 0, 4, 1, alignment=Qt.AlignCenter)
        
        fileUpload = FileUploadButton()
        self.mainLayout.addWidget(fileUpload, 3, 0, 4, 1, alignment=Qt.AlignCenter)
        
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)