from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3

class LoginPage(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        title = QLabel('Login')
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

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet('''
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

        signup_layout = QHBoxLayout()
        signup_label = QLabel("Don't have an account?")
        signup_label.setStyleSheet('font-size: 14px;')

        self.signup_button = QPushButton('Sign Up')
        self.signup_button.clicked.connect(self.showSignupPage)
        self.signup_button.setStyleSheet('''
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

        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(self.signup_button)

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.addLayout(signup_layout)
        layout.setAlignment(signup_layout, Qt.AlignCenter)

        self.setLayout(layout)
        self.setStyleSheet('background-color: #f0f0f0;')

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        cursor = self.main_app.conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()

        if user:
            self.main_app.user_id = user[0]
            if username == 'admin' and password == 'admin123':
                self.main_app.showAdminPage()
            else:
                self.main_app.showMainPage()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

    def showSignupPage(self):
        self.main_app.showSignupPage()
