import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class SignupPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Signup')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label_username = QLabel('Username:', self)
        layout.addWidget(self.label_username)

        self.textbox_username = QLineEdit(self)
        layout.addWidget(self.textbox_username)

        self.label_password = QLabel('Password:', self)
        layout.addWidget(self.label_password)

        self.textbox_password = QLineEdit(self)
        self.textbox_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.textbox_password)

        self.button_signup = QPushButton('Signup', self)
        self.button_signup.clicked.connect(self.signup)
        layout.addWidget(self.button_signup)

        self.setLayout(layout)

    def signup(self):
        username = self.textbox_username.text()
        password = self.textbox_password.text()

        if self.create_user(username, password):
            QMessageBox.information(self, 'Success', 'Account created successfully.')
            self.main_app.showLoginPage()
        else:
            QMessageBox.warning(self, 'Error', 'Username already exists.')

    def create_user(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success
