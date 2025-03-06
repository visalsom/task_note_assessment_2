from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QMessageBox, QStackedWidget, QSystemTrayIcon)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from ui.login_dialog import LoginDialog
from ui.task_list_form import TaskListForm
from ui.crud_task_form import CrudTaskForm
from database.db import Database
from styles.styles import STYLESHEET
import datetime


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.user_id = None
        self.init_system_tray()
        self.show_login()

    def init_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # You'll need to provide an icon file
        self.tray_icon.setVisible(True)

    def show_login(self):
        login_dialog = LoginDialog()
        if login_dialog.exec():
            username = login_dialog.username.text()
            password = login_dialog.password.text()

            self.user_id = self.db.verify_user(username, password)
            if not self.user_id:
                self.user_id = self.db.register_user(username, password)
                if not self.user_id:
                    QMessageBox.warning(self, "Error", "Username taken or login failed")
                    self.close()
                    return
                QMessageBox.information(self, "Success", "User registered successfully")

            self.initUI()
            self.start_notification_timer()
            self.show()
        else:
            self.close()

    def initUI(self):
        self.setWindowTitle('Task Note Manager')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Navigation bar
        nav_layout = QHBoxLayout()

        self.task_list_btn = QPushButton("Task List")
        self.task_list_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        nav_layout.addWidget(self.task_list_btn)

        self.crud_task_btn = QPushButton("Manage Tasks")
        self.crud_task_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        nav_layout.addWidget(self.crud_task_btn)

        self.logout_btn = QPushButton(" ⟳ Logout")
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn.setObjectName("logout_btn")
        nav_layout.addWidget(self.logout_btn)

        layout.addLayout(nav_layout)

        # Stacked widget for forms
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Initialize forms
        self.task_list_form = TaskListForm(self.user_id, self.db)
        self.crud_task_form = CrudTaskForm(self.user_id, self.db)

        # Add forms to stacked widget
        self.stacked_widget.addWidget(self.task_list_form)
        self.stacked_widget.addWidget(self.crud_task_form)

        # Connect signals between forms
        self.crud_task_form.task_updated.connect(self.task_list_form.load_tasks)

        self.setStyleSheet(STYLESHEET)

    def start_notification_timer(self):
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.check_due_tasks)
        self.notification_timer.start(3600000)  # Check every hour (3600 seconds)
        self.check_due_tasks()  # Check immediately on startup

    def check_due_tasks(self):
        tasks = self.db.get_user_tasks(self.user_id)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        for task in tasks:
            task_id, title, _, due_date, _, status, _ = task  # Updated to unpack 7 values
            if due_date == tomorrow and status != "Completed":
                self.tray_icon.showMessage(
                    "Task Due Tomorrow",
                    f"Task '{title}' is due tomorrow!",
                    QSystemTrayIcon.MessageIcon.Information,
                    5000  # Display for 5 seconds
                )

    def logout(self):
        self.notification_timer.stop()
        self.user_id = None
        self.close()
        self.show_login()