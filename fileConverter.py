import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from pdf2docx import parse
from docx2pdf import convert

class FileConverter(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.initUI()
        self.main_app = main_app

    def initUI(self):
        self.setWindowTitle('File Converter')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Select a conversion option:', self)
        self.label.setAlignment(Qt.AlignCenter)  # Center align the label text
        layout.addWidget(self.label)

        self.button_pdf_to_doc = QPushButton('Convert PDF to DOCX', self)
        self.button_pdf_to_doc.clicked.connect(self.convertPdfToDocx)
        layout.addWidget(self.button_pdf_to_doc)

        self.button_doc_to_pdf = QPushButton('Convert DOCX to PDF', self)
        self.button_doc_to_pdf.clicked.connect(self.convertDocToPdf)
        layout.addWidget(self.button_doc_to_pdf)

        # Button to go back to home
        self.button_back = QPushButton('Back to Home', self)
        self.button_back.clicked.connect(self.goBackToHome)
        layout.addWidget(self.button_back)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;  /* Light gray background */
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QPushButton {
                font-size: 14px;
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 10px;
                background-color: #4CAF50;  /* Green */
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #3e8e41;  /* Darker green when pressed */
            }
        """)

    def convertPdfToDocx(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)", options=options)
        if fileName:
            output_file = fileName.replace('.pdf', '.docx')
            parse(fileName, output_file)
            QMessageBox.information(self, 'Success', f'Converted to {output_file}')
            self.storeFileInDatabase(output_file)

    def convertDocToPdf(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select DOCX File", "", "DOCX Files (*.docx)", options=options)
        if fileName:
            convert(fileName)
            output_file = fileName.replace('.docx', '.pdf')
            QMessageBox.information(self, 'Success', f'Converted to {output_file}')
            self.storeFileInDatabase(output_file)

    def storeFileInDatabase(self, file_path):
        if self.main_app and self.main_app.user_id is not None:
            file_name = os.path.basename(file_path)
            self.main_app.store_generated_file(self.main_app.user_id, file_name, file_path)
        else:
            QMessageBox.warning(self, 'Error', 'Main application reference or user ID not found.')

    def goBackToHome(self):
        if self.main_app:
            self.main_app.showMainPage()  # Call the method to show the main page
        else:
            QMessageBox.warning(self, 'Error', 'Main application reference not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from main import MainApp
    main_app = MainApp()
    file_converter = FileConverter(main_app=main_app)
    file_converter.show()
    sys.exit(app.exec_())
