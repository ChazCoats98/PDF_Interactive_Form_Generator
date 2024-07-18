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
        
        
        self.uploadButton = UploadButton('Upload File')
        self.uploadButton.setFixedSize(100, 30)
        animation_properties = [
            ('minimumSize', QSize(200, 200)),
            ('color', QColor(191, 223, 255)),
            ('opacity', .5)
        ]
        duration = 500
        
        self.growAnim = QParallelAnimationGroup()
        
        for property, value in animation_properties:
            self.anim = QPropertyAnimation(self.uploadButton, bytes(property, 'utf8'))
            self.anim.setEndValue(value)
            self.anim.setDuration(duration)
            self.growAnim.addAnimation(self.anim)
        
        layout.addWidget(self.uploadButton)
                
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.growAnim.start()
            self.uploadButton.setText('Drop File')
            
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.uploadButton.setText('Upload File')
            
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.file.append(url.toLocalFile())
            
class UploadButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._color = QColor('white') 
        
    def getColor(self):
        return self._color
    
    def setColor(self, color):
        self._color = color
        self.setStyleSheet(f"background-color: {color.name()}")
        
    color = pyqtProperty(QColor, getColor, setColor)