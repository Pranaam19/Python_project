from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QApplication
from PyQt5.QtCore import Qt

class EmailTemplateGenerator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

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

        self.setLayout(layout)

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
