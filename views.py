from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets import UploadFileBox

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Interactive Form Generator')
        self.resize(200, 200)
        
        self.setContentsMargins(40, 40, 40, 40)
        
        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout(self.mainWidget)
        
        self.dropLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.dropLayout, 1, 0, 4, 2)
        
        self.logo = QPixmap('./assets/interactive_form_logo.png')
        self.logo = self.logo.scaled(350, 200)
        tagline = QLabel(self)
        tagline.setPixmap(self.logo)
        self.mainLayout.addWidget(tagline, 0, 0, 1, 1, alignment=Qt.AlignCenter)
        
        fileUpload = UploadFileBox()
        self.dropLayout.addWidget(fileUpload)
        
        self.setCentralWidget(self.mainWidget)