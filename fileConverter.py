import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from pdf2docx import parse
from docx2pdf import convert

class FileConverter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Converter')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Select a conversion option:', self)
        layout.addWidget(self.label)

        self.button_pdf_to_doc = QPushButton('Convert PDF to DOCX', self)
        self.button_pdf_to_doc.clicked.connect(self.convertPdfToDocx)
        layout.addWidget(self.button_pdf_to_doc)

        self.button_doc_to_pdf = QPushButton('Convert DOCX to PDF', self)
        self.button_doc_to_pdf.clicked.connect(self.convertDocToPdf)
        layout.addWidget(self.button_doc_to_pdf)

        self.setLayout(layout)

    def convertPdfToDocx(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)", options=options)
        if fileName:
            output_file = fileName.replace('.pdf', '.docx')
            parse(fileName, output_file)
            QMessageBox.information(self, 'Success', f'Converted to {output_file}')

    def convertDocToPdf(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select DOCX File", "", "DOCX Files (*.docx)", options=options)
        if fileName:
            convert(fileName)
            output_file = fileName.replace('.docx', '.pdf')
            QMessageBox.information(self, 'Success', f'Converted to {output_file}')
