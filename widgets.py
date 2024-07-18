import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FileUploadButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Upload Files", parent)
        self.setAcceptDrops(True)
        self.file = []
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.file.append(url.toLocalFile())
            self.setText(f'{len(self.file)} files uploaded')
            event.acceptProposedAction()
            
    def getFiles(self):
        return self.file