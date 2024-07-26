from PyQt5.QtCore import QObject
import fitz
import re
import io
import os
from PyPDF2 import PdfReader, PdfWriter
from collections import defaultdict
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import win32com.client


class Worker(QObject):
    finished = pyqtSignal()
    init_file_dialog = pyqtSignal(str)
    
    def __init__(self, filePath, parent = None):
        super().__init__(parent)
        self.original_filename = self.get_original_filename(filePath)
        self.output_pdf = None
        self.filePath = filePath
        self.parent = parent
        
    def run(self):
        self.handle_doctype(self.parent, self.filePath)
        
    def get_text_width(self, text, font_name, font_size):
        font = fitz.Font()
        point_width = font.text_length(text, font_size)
        return point_width
    
    
    def extract_pdf(self, filename):
        document = fitz.open(filename)
        markers = []

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text = page.get_text('dict')
            lineNum = 0
        
            for block in text['blocks']:
                for line in block['lines']:
                    for span in line['spans']:
                        if re.search(r'[\uf0a8\uf0f0]', span["text"]):
                            markers.append({
                                "type": "radio",
                                "x": span["bbox"][0],
                                "y": span["bbox"][3],
                                "size": span["size"],
                                "page_num": page_num
                            })
                        else:
                            bracket_matches = re.finditer(r'\[([^\]]*)\]', span['text'])
                            for match in bracket_matches:
                                start_index = match.start()
                                end_index = match.end()

                                preceding_text = span['text'][:start_index]
                                bracket_text = span['text'][start_index:end_index]
                                
                                
                                preceding_text_width = self.get_text_width(preceding_text, span['font'], span['size'])
                                bracket_text_width = self.get_text_width(bracket_text, span['font'], span['size'])
                                #print(f'preceding text: {preceding_text}, preceding text width: {preceding_text_width}')
                                #print(f'bracket text: {bracket_text}, bracket text width: {bracket_text_width}')

                                start_x = span['bbox'][0] + preceding_text_width
                                width = bracket_text_width
                                height = span['bbox'][3] - span['bbox'][1]
                                lineNum += 1
                                #print(f'bbox: {span} bbox x 0: {span['bbox'][0]}')
                                #print(f'Start x: {start_x}')

                                markers.append({
                                    "type": "text",
                                    "x": start_x,
                                    "y": span['bbox'][3],
                                    "width": width,
                                    'height': height,
                                    "page_num": page_num
                                    })
        #print(markers)                
        self.create_interactive_pdf(filename, markers)
                        
    def create_interactive_pdf(self, original_file, markers):
        original_pdf = PdfReader(open(original_file, 'rb'))
        self.output_pdf = PdfWriter()
    
        for i in range(len(original_pdf.pages)):
            original_page = original_pdf.pages[i]
            original_page_width = original_page.mediabox[2]
            original_page_height = original_page.mediabox[3]
        
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(original_page_width, original_page_height))
            acroform = can.acroForm
    
            radio_buttons = defaultdict(list)
            for marker in markers:
                if marker["type"] == "radio":
                    radio_buttons[(marker["page_num"], marker["y"])].append(marker)
            
            counter = 1
    
            for (page_num, y_value), group in radio_buttons.items():
                group_name = f"RadioGroup{counter}"
                counter += 1
                for marker in group:
                    acroform.radio(
                        name=group_name,
                        value=f"Option{marker['x']}",
                        x=marker['x'] - (marker['size'] / 2),
                        y=original_page_height - (marker['y'] + (marker['size'] / 4) - .5),
                        size= (marker['size'] * 1.5),
                        buttonStyle="cross",
                        shape="square",
                        borderWidth=.5,
                        selected=False,
                    )
            text_counter = 1
            for marker in markers:
                text_counter += 1
                if marker["type"] == "text":
                    acroform.textfield(
                        name=f"TextField{text_counter}",
                        x=marker['x'],
                        y=original_page_height - marker['y'],
                        width=marker['width'],
                        height=marker['height'],
                        borderStyle="solid",
                        borderWidth=1,
                        forceBorder=True,
                        maxlen=50            
                    )
            
            can.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)
            page = original_pdf.pages[i]
            if new_pdf.pages[0]:
                page.merge_page(new_pdf.pages[0])
        
            self.output_pdf.add_page(page)
            
        self.init_file_dialog.emit(self.original_filename)
        
    def xlsx_to_pdf(self, document):
        output_file = './temp/temp_pdf.pdf'
    
        ex = win32com.client.Dispatch('Excel.Application')
        ex.Visible = False
        ex.DisplayAlerts = False
    
        workbook = ex.Workbooks.Open(document)
    
        workbook.ExportAsFixedFormat(0, os.path.abspath(output_file))
    
        workbook.Close()
        ex.quit()
    
        self.extract_pdf(output_file)
        
    def doc_to_pdf(self, document):
        output_file = './temp/temp_pdf.pdf'
    
        wd = win32com.client.Dispatch('Word.Application')
        wd.Visible = True
        wd.DisplayAlerts = False
    
        doc = wd.Documents.Open(document)
    
        doc.ExportAsFixedFormat(OutputFileName=os.path.abspath(output_file), ExportFormat=17)
    
        doc.Close()
        wd.Quit()
    
        self.extract_pdf(output_file)
        
    def get_original_filename(self, filePath):
        filedata = filePath.split('/')
        for f in filedata:
            if f.endswith('.xlsx') or f.endswith('.docx') or f.endswith('.doc') or f.endswith('.pdf'):
                original_filename = f.split('.')[0]
                
        return original_filename
            
    
    def handle_doctype(self, parent, filePath):
        if filePath.endswith('.xlsx'):
            self.xlsx_to_pdf(filePath)
        elif filePath.endswith('.docx') or filePath.endswith('.doc'):
            self.doc_to_pdf(filePath)
        elif filePath.endswith('.pdf'):
            self.extract_pdf(filePath)
        else:
            showFileError(parent)
        
def showFileError(self, parent):
    dlg = QMessageBox(parent)
    dlg.setWindowTitle('ERROR')
    dlg.setText('Invalid file type. \nFile must be an Excel, Word, or PDF file.')
    dlg.setIcon(QMessageBox.Warning)
    dlg.exec()
        