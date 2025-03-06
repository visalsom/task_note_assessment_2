from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QLabel


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)

        layout = QFormLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow(QLabel("Username:"), self.username)
        layout.addRow(QLabel("Password:"), self.password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.accept)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)