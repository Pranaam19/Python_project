from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3

class SignupPage(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sign Up')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        title = QLabel('Sign Up')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setStyleSheet('color: #4CAF50; margin-bottom: 20px;')
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setStyleSheet('padding: 10px; border-radius: 5px; border: 1px solid #ccc;')

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setStyleSheet('padding: 10px; border-radius: 5px; border: 1px solid #ccc;')

        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)

        self.signup_button = QPushButton('Sign Up')
        self.signup_button.clicked.connect(self.signup)
        self.signup_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                margin-top: 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')

        login_layout = QHBoxLayout()
        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet('font-size: 14px;')

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.showLoginPage)
        self.login_button.setStyleSheet('''
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 14px;
                padding: 5px 15px;
                margin-left: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        ''')

        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.signup_button, alignment=Qt.AlignCenter)
        layout.addLayout(login_layout)
        layout.setAlignment(login_layout, Qt.AlignCenter)

        self.setLayout(layout)
        self.setStyleSheet('background-color: #f0f0f0;')

    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        cursor = self.main_app.conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.main_app.conn.commit()
            QMessageBox.information(self, 'Success', 'Account created successfully')
            self.main_app.showLoginPage()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Username already exists')

    def showLoginPage(self):
        self.main_app.showLoginPage()
