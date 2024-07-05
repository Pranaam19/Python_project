from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet

class DigitalKeyGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Digital Key Generator')
        self.setGeometry(100, 100, 800, 400)

        self.layout = QVBoxLayout()

        # Add title label
        self.title_label = QLabel('Digital Key Generator', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size: 24px; font-weight: bold; padding: 20px;')
        self.layout.addWidget(self.title_label)

        # Add generate key button
        self.btn_generate_key = QPushButton('Generate Digital Key', self)
        self.btn_generate_key.clicked.connect(self.generateDigitalKey)
        self.style_button(self.btn_generate_key)
        self.layout.addWidget(self.btn_generate_key)

        # Add encrypt file button
        self.btn_encrypt_file = QPushButton('Encrypt File', self)
        self.btn_encrypt_file.clicked.connect(self.encryptFile)
        self.style_button(self.btn_encrypt_file)
        self.layout.addWidget(self.btn_encrypt_file)

        # Add decrypt file button
        self.btn_decrypt_file = QPushButton('Decrypt File', self)
        self.btn_decrypt_file.clicked.connect(self.decryptFile)
        self.style_button(self.btn_decrypt_file)
        self.layout.addWidget(self.btn_decrypt_file)

        self.setLayout(self.layout)

        # Apply background color to the page
        self.setStyleSheet('background-color: #f0f0f0;')

    def style_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 18px;
                margin: 20px;
                width: 300px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green */
            }
        ''')

    def generateDigitalKey(self):
        key = Fernet.generate_key()
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "Save Digital Key", "", "Key Files (*.key)")

        if save_path:
            try:
                with open(save_path, 'wb') as key_file:
                    key_file.write(key)
                QMessageBox.information(self, "Success", "Digital key successfully generated and saved!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the digital key: {e}")

    def encryptFile(self):
        key_file_dialog = QFileDialog()
        key_path, _ = key_file_dialog.getOpenFileName(self, "Select Key File", "", "Key Files (*.key)")

        if key_path:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()

            fernet = Fernet(key)

            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Select File to Encrypt", "")

            if file_path:
                with open(file_path, 'rb') as file:
                    file_data = file.read()

                encrypted_data = fernet.encrypt(file_data)

                save_path, _ = file_dialog.getSaveFileName(self, "Save Encrypted File", "", "Encrypted Files (*.enc)")

                if save_path:
                    try:
                        with open(save_path, 'wb') as enc_file:
                            enc_file.write(encrypted_data)
                        QMessageBox.information(self, "Success", "File successfully encrypted!")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"An error occurred while saving the encrypted file: {e}")

    def decryptFile(self):
        key_file_dialog = QFileDialog()
        key_path, _ = key_file_dialog.getOpenFileName(self, "Select Key File", "", "Key Files (*.key)")

        if key_path:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()

            fernet = Fernet(key)

            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Select File to Decrypt", "", "Encrypted Files (*.enc)")

            if file_path:
                with open(file_path, 'rb') as enc_file:
                    encrypted_data = enc_file.read()

                try:
                    decrypted_data = fernet.decrypt(encrypted_data)

                    save_path, _ = file_dialog.getSaveFileName(self, "Save Decrypted File", "")

                    if save_path:
                        with open(save_path, 'wb') as dec_file:
                            dec_file.write(decrypted_data)
                        QMessageBox.information(self, "Success", "File successfully decrypted!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while decrypting the file: {e}")
