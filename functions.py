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

def extract_pdf(self, filename):
    document = fitz.open(filename)
    markers = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text('dict')
        
        for block in text['blocks']:
            for line in block['lines']:
                for span in line['spans']:
                    if re.search(r'[\uf0a8\uf0f0]', span["text"]):
                        markers.append({
                            "type": "radio",
                            "x": span["bbox"][0],
                            "y": span["bbox"][1],
                            "size": span["size"],
                            "page_num": page_num
                        })
                    elif "___" in span["text"]:
                        if 'Signature' not in span["text"]:
                            underscore_matches = re.finditer(r'_{3,}', span["text"])
                            for match in underscore_matches:
                            
                                start_index = match.start()
                                end_index = match.end()

                                preceding_text_width = fitz.get_text_length(span["text"][:start_index])
                                underscore_width = fitz.get_text_length(span["text"][start_index:end_index])

                                start_x = span['bbox'][0] + preceding_text_width
                                end_x = start_x + underscore_width
                                width = end_x - start_x

                                markers.append({
                                    "type": "text",
                                    "x": start_x,
                                    "y": span['bbox'][1],
                                    "width": width,
                                    "page_num": page_num
                                })                 
    create_interactive_pdf(self, filename, markers)
                        
def create_interactive_pdf(self, original_file, markers):
    original_pdf = PdfReader(open(original_file, 'rb'))
    output_pdf = PdfWriter()
    
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
                    x=marker['x'],
                    y=original_page_height - (marker['y'] + marker['size'] + 2),
                    size= (marker['size'] + 2),
                    buttonStyle="cross",
                    shape="square",
                    selected=False,
                )
        text_counter = 1
        for marker in markers:
            text_counter += 1
            if marker["type"] == "text":
                acroform.textfield(
                    name=f"TextField{text_counter}",
                    x=marker['x'] - 5,
                    y=original_page_height - (marker['y'] + 10),
                    width=marker['width'],
                    height=20,
                    borderStyle="solid",
                    borderWidth=1,
                    forceBorder=True,
                    maxlen=50            
                )
            
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        page = original_pdf.pages[i]
        page.merge_page(new_pdf.pages[0])
        
        output_pdf.add_page(page)
        
    basePath = f'//server/D/Quality Control'
    fileName, ok = QFileDialog.getSaveFileName(
                self,
                "Save Excel File",
                basePath,
                "PDF Files (*.pdf)")
            
    if fileName:
        with open(fileName, "wb") as f:
            output_pdf.write(f)
        self.file += 1
        self.uploadButton.setText(f'{self.file} files converted')
        
def xlsx_to_pdf(self, document):
    output_file = './temp/temp_pdf.pdf'
    
    ex = win32com.client.Dispatch('Excel.Application')
    ex.Visible = False
    
    workbook = ex.Workbooks.Open(document)
    
    workbook.ExportAsFixedFormat(0, os.path.abspath(output_file))
    
    workbook.Close()
    ex.quit()
    
    extract_pdf(self, output_file)
    
def open_file_explorer(self):
    basePath = f'//server/D/Scanned images'
    filePath, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Form File", 
            basePath
        )
    
    if filePath.endswith('.xlsx'):
        xlsx_to_pdf(self, filePath)
    elif filePath.endswith('.docx') or filePath.endswith('.doc'):
        print('ehhhh... docx conversion to be implemented soon i guess')
    elif filePath.endswith('.pdf'):
        extract_pdf(self, filePath)
    else:
        showFileError(self)
        
def showFileError(self):
    dlg = QMessageBox(self)
    dlg.setWindowTitle('ERROR')
    dlg.setText('Invalid file type. \nFile must be an Excel, Word, or PDF file.')
    dlg.setIcon(QMessageBox.Warning)
    dlg.exec()