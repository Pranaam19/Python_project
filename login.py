from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Store the parent widget (MainApp)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Page')
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel('Login to MyApp', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 32px; font-weight: bold; color: #232f3e; margin-bottom: 20px;')
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        username_label = QLabel('Username:', self)
        username_label.setStyleSheet('font-size: 18px; color: #232f3e;')
        form_layout.addWidget(username_label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setStyleSheet('padding: 10px; border-radius: 5px; border: 1px solid #cccccc;')
        form_layout.addWidget(self.username_input)

        password_label = QLabel('Password:', self)
        password_label.setStyleSheet('font-size: 18px; color: #232f3e;')
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet('padding: 10px; border-radius: 5px; border: 1px solid #cccccc;')
        form_layout.addWidget(self.password_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.login)
        login_button.setStyleSheet('''
            QPushButton {
                background-color: #ff9900;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 5px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #e68a00;
            }
        ''')
        button_layout.addWidget(login_button)

        signup_button = QPushButton('Sign Up', self)
        signup_button.clicked.connect(self.showSignupPage)
        signup_button.setStyleSheet('''
            QPushButton {
                background-color: #232f3e;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1e272e;
            }
        ''')
        button_layout.addWidget(signup_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Input Error', 'Please fill out all fields')
            return

        try:
            conn = sqlite3.connect('myapp.db')
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
            result = cursor.fetchone()

            if result:
                self.parent_widget.user_id = result[0]
                self.parent_widget.showMainPage()
            else:
                QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')

        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Database Error', f'Database error occurred: {str(e)}')

        finally:
            if conn:
                conn.close()

    def showSignupPage(self):
        self.parent_widget.showSignupPage()
