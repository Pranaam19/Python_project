import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class AdminPage(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin Page')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # Navbar
        navbar_layout = QHBoxLayout()
        navbar_layout.setAlignment(Qt.AlignTop)

        logo_label = QLabel('Admin Page', self)
        logo_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #ffffff;')
        navbar_layout.addWidget(logo_label)

        back_button = QPushButton('Back to Home', self)
        back_button.setStyleSheet('background-color: #0078d7; color: white; padding: 10px 20px; border-radius: 5px;')
        back_button.clicked.connect(self.main_app.showMainPage)
        navbar_layout.addWidget(back_button)

        main_layout.addLayout(navbar_layout)

        # Content Section
        content_layout = QVBoxLayout()

        # User List Widget
        self.user_list = QListWidget(self)
        self.load_users()
        content_layout.addWidget(self.user_list)

        # Form Layout for Adding Users
        form_layout = QFormLayout()

        self.new_username_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow('New Username:', self.new_username_input)
        form_layout.addRow('New Password:', self.new_password_input)

        # Buttons for Adding and Deleting Users
        add_user_button = QPushButton('Add User')
        add_user_button.clicked.connect(self.add_user)
        add_user_button.setStyleSheet('background-color: #4CAF50; color: white; padding: 10px 20px; border-radius: 5px;')
        form_layout.addWidget(add_user_button)

        delete_user_button = QPushButton('Delete Selected User')
        delete_user_button.clicked.connect(self.delete_user)
        delete_user_button.setStyleSheet('background-color: #f44336; color: white; padding: 10px 20px; border-radius: 5px;')
        form_layout.addWidget(delete_user_button)

        content_layout.addLayout(form_layout)
        content_layout.setAlignment(Qt.AlignTop)

        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        # Apply Styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-bottom: 10px;
                min-height: 200px;
            }
            QFormLayout {
                margin: 20px;
            }
            QLineEdit, QPushButton {
                font-size: 16px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 3px;
                margin-bottom: 10px;
            }
            QPushButton {
                min-width: 120px;
            }
            QLabel {
                font-size: 14px;
            }
        """)

    def load_users(self):
        self.user_list.clear()
        cursor = self.main_app.conn.cursor()
        cursor.execute('SELECT id, username FROM users')
        users = cursor.fetchall()
        for user in users:
            self.user_list.addItem(f"{user[0]}: {user[1]}")

    def add_user(self):
        username = self.new_username_input.text()
        password = self.new_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        cursor = self.main_app.conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.main_app.conn.commit()
            QMessageBox.information(self, 'Success', 'User added successfully')
            self.load_users()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Username already exists')

    def delete_user(self):
        selected_user = self.user_list.currentItem()
        if selected_user:
            user_id = int(selected_user.text().split(':')[0])
            cursor = self.main_app.conn.cursor()
            cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
            self.main_app.conn.commit()
            QMessageBox.information(self, 'Success', 'User deleted successfully')
            self.load_users()
        else:
            QMessageBox.warning(self, 'Error', 'No user selected')
