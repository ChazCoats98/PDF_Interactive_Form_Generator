import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
    
class UploadFileBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(350, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)

        self.file = []
        
        self.initUi()
        
    
    def initUi(self):    
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 200)
        layout.setAlignment(Qt.AlignCenter)
        
        self.uploadButton = QPushButton('Upload File')
        self.uploadButton.setFixedSize(100, 30)
        layout.addWidget(self.uploadButton)
        
        
                
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.uploadButton.setText('Drop File')
            
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.uploadButton.setText('Upload File')
            
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.file.append(url.toLocalFile())
            