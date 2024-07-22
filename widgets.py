import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functions import *
    
class UploadFileBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 200)
        self.file = 0
        self.parent = parent
        self.thread = None
        
        self.initUi()
        
    
    def initUi(self):    
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 200)
        layout.setAlignment(Qt.AlignCenter)
        
        
        self.uploadButton = UploadButton('Upload File')
        self.uploadButton.setFixedSize(100, 30)
        
        self.opacityEffect = QGraphicsOpacityEffect()
        self.uploadButton.setGraphicsEffect(self.opacityEffect)
        self.uploadButton.clicked.connect(self.open_file_explorer)
        
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
                self.shrinkAnim.start()
                self.startThread(url.toLocalFile())
                self.uploadButton.setText('Upload File')
                
    def open_file_explorer(self):
        basePath = f'//server/D/Scanned images'
        filePath, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Form File", 
            basePath
        )
        if filePath:
            self.startThread(filePath)
    
    def startThread(self, filePath):
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
            
        self.thread = QThread()
        self.worker = Worker(filePath)
        self.worker.moveToThread(self.thread)
                
        self.worker.init_file_dialog.connect(self.openFileDialog)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
                
    @pyqtSlot(str)
    def openFileDialog(self, original_filename):
        fileName, ok = QFileDialog.getSaveFileName(
            self,
            "Save Form File",
            original_filename,
            "PDF Files (*.pdf)")
            
        if fileName:
            with open(fileName, "wb") as f:
                self.worker.output_pdf.write(f)
            self.file += 1
            self.uploadButton.setText(f'{self.file} files converted')
            self.worker.finished.emit()
        
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
    