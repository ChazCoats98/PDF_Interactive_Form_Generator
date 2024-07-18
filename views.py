from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets import UploadFileBox

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Interactive Form Generator')
        self.resize(200, 100)
        
        self.setContentsMargins(40, 40, 40, 40)
        
        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout(self.mainWidget)
        
        
        self.logo = QPixmap('./assets/interactive_form_logo_70.png')
        tagline = QLabel(self)
        tagline.setPixmap(self.logo)
        self.mainLayout.addWidget(tagline, 0, 0, 1, 1, alignment=Qt.AlignCenter)
        
        guideline = QLabel('Drop or upload an Excel, Word, or PDF file below to convert it to an interactive form')
        self.mainLayout.addWidget(guideline, 1, 0, 1, 1, alignment=Qt.AlignCenter)
        
        self.dropLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.dropLayout, 2, 0, 1, 1)
        fileUpload = UploadFileBox()
        self.dropLayout.addWidget(fileUpload)
        
        self.mainLayout.setRowStretch(2, 200)
        self.mainLayout.setColumnStretch(0, 1)
        
        self.setCentralWidget(self.mainWidget)