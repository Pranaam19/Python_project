from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from pdf2docx import Converter as PDFToDocxConverter
from docx2pdf import convert as DocxToPDFConverter

class FileConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Converter')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel('Choose a file conversion option:', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        btn_pdf_to_docx = QPushButton('Convert PDF to DOCX', self)
        btn_pdf_to_docx.clicked.connect(self.convertPDFToDocx)
        layout.addWidget(btn_pdf_to_docx)

        btn_docx_to_pdf = QPushButton('Convert DOCX to PDF', self)
        btn_docx_to_pdf.clicked.connect(self.convertDocxToPDF)
        layout.addWidget(btn_docx_to_pdf)

        self.setLayout(layout)

    def convertPDFToDocx(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        pdf_file, _ = QFileDialog.getOpenFileName(self, "Select PDF file to convert", "", "PDF Files (*.pdf)", options=options)
        if pdf_file:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save DOCX file", "", "DOCX Files (*.docx)", options=options)
            if save_path:
                try:
                    converter = PDFToDocxConverter(pdf_file)
                    converter.convert(save_path, start=0, end=None)
                    converter.close()
                    QMessageBox.information(self, "Success", "PDF successfully converted to DOCX")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while converting PDF to DOCX: {e}")

    def convertDocxToPDF(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        docx_file, _ = QFileDialog.getOpenFileName(self, "Select DOCX file to convert", "", "DOCX Files (*.docx)", options=options)
        if docx_file:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF file", "", "PDF Files (*.pdf)", options=options)
            if save_path:
                try:
                    DocxToPDFConverter(docx_file, save_path)
                    QMessageBox.information(self, "Success", "DOCX successfully converted to PDF")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while converting DOCX to PDF: {e}")
