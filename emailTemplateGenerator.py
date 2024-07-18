import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QApplication, QMessageBox
from PyQt5.QtCore import Qt

class EmailTemplateGenerator(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.initUI()
        self.main_app = main_app

    def initUI(self):
        self.setWindowTitle('Email Template Generator')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label_subject = QLabel('Email Subject:', self)
        layout.addWidget(self.label_subject)

        self.textbox_subject = QLineEdit(self)
        layout.addWidget(self.textbox_subject)

        self.label_context = QLabel('Context:', self)
        layout.addWidget(self.label_context)

        self.textbox_context = QTextEdit(self)
        layout.addWidget(self.textbox_context)

        self.button_generate = QPushButton('Generate Email Template', self)
        self.button_generate.clicked.connect(self.generateEmailTemplate)
        layout.addWidget(self.button_generate)

        self.label_template = QLabel('Generated Template:', self)
        layout.addWidget(self.label_template)

        self.textbox_template = QTextEdit(self)
        self.textbox_template.setReadOnly(True)
        layout.addWidget(self.textbox_template)

        self.button_copy = QPushButton('Copy Template', self)
        self.button_copy.clicked.connect(self.copyTemplate)
        layout.addWidget(self.button_copy)

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
            QLineEdit, QTextEdit {
                font-size: 14px;
                padding: 10px;
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

    def generateEmailTemplate(self):
        subject = self.textbox_subject.text()
        context = self.textbox_context.toPlainText()

        if subject and context:
            template = f"Subject: {subject}\n\nDear [Recipient],\n\n{context}\n\nBest regards,\n[Your Name]"
        else:
            template = "Please provide both subject and context."

        self.textbox_template.setPlainText(template)

    def copyTemplate(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textbox_template.toPlainText())

    def goBackToHome(self):
        if self.main_app:
            self.main_app.showMainPage()  # Call the method to show the main page
        else:
            QMessageBox.warning(self, 'Error', 'Main application reference not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from main import MainApp
    main_app = MainApp()
    email_template_generator = EmailTemplateGenerator(main_app=main_app)
    email_template_generator.show()
    sys.exit(app.exec_())
