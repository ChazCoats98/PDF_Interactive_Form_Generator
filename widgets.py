import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
    
class UploadFileBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.file = []
        
        self.initUi()
        
    
    def initUi(self):    
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 200)
        layout.setAlignment(Qt.AlignCenter)
        
        
        self.uploadButton = UploadButton('Upload File')
        self.uploadButton.setFixedSize(100, 30)
        
        self.opacityEffect = QGraphicsOpacityEffect()
        self.uploadButton.setGraphicsEffect(self.opacityEffect)
        
        self.default_properties = {
            'minimumSize': self.uploadButton.minimumSize(),
            'color': QColor(240, 240, 240),
            'opacity': 1,
            'borderWidth': 1
        }
        
        animation_properties = [
            (self.uploadButton, 'minimumSize', QSize(200, 200)),
            (self.uploadButton,'color', QColor(191, 223, 255)),
            (self.opacityEffect,'opacity', .5),
            (self.uploadButton,'borderWidth', 0)
        ]
        self.duration = 200
        
        self.growAnim = QParallelAnimationGroup()
        self.shrinkAnim = QParallelAnimationGroup()
        
        for item, property, value in animation_properties:
            self.initAnim(item, property, value)
        
        layout.addWidget(self.uploadButton)
        
    def initAnim(self, item, property, value):
        anim = QPropertyAnimation(item, bytes(property, 'utf8'))
        anim.setEndValue(value)
        anim.setDuration(self.duration)
        self.growAnim.addAnimation(anim)
        
        print(property, anim.startValue())
        
        reverseAnim = QPropertyAnimation(item, bytes(property, 'utf8'))
        reverseAnim.setEndValue(self.default_properties[property])
        reverseAnim.setDuration(self.duration)
        self.shrinkAnim.addAnimation(reverseAnim) 
                
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.growAnim.start()
            self.uploadButton.setText('Drop File')
            
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.uploadButton.setText('Upload File')
        self.shrinkAnim.start()
            
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.file.append(url.toLocalFile())
            
class UploadButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._color = QColor('white')
        self._border_width = 1
        
    def getColor(self):
        return self._color
    
    def getBorderWidth(self):
        return self._border_width
    
    def setColor(self, color):
        self._color = color
        self.updateStyleSheet()
        
    def setBorderWidth(self, width):
        self._border_width = width
        self.updateStyleSheet()
        
    def updateStyleSheet(self):
        self.setStyleSheet(f"border: {self._border_width}px solid; background-color: {self.color.name()}")
        
    color = pyqtProperty(QColor, getColor, setColor)
    borderWidth = pyqtProperty(int, getBorderWidth, setBorderWidth)