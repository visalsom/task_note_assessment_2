from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QPushButton, QLineEdit, QTextEdit, QMessageBox,
                             QLabel, QDateEdit, QComboBox, QSpinBox, QListWidgetItem)
from PyQt6.QtCore import Qt, QDate, pyqtSignal


class CrudTaskForm(QWidget):
    task_updated = pyqtSignal()

    def __init__(self, user_id, db):
        super().__init__()
        self.user_id = user_id
        self.db = db
        self.all_tasks = []
        self.initUI()
        self.load_tasks()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter tasks by title...")
        self.search_input.textChanged.connect(self.filter_tasks)
        left_layout.addWidget(self.search_input)

        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self.task_selected)
        left_layout.addWidget(self.task_list)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        title_label = QLabel("Task Title")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")
        right_layout.addWidget(title_label)
        right_layout.addWidget(self.title_input)

        desc_label = QLabel("Task Description")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Enter task description")
        right_layout.addWidget(desc_label)
        right_layout.addWidget(self.desc_input)

        due_date_label = QLabel("Due Date")
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        right_layout.addWidget(due_date_label)
        right_layout.addWidget(self.due_date_input)

        priority_label = QLabel("Priority")
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        right_layout.addWidget(priority_label)
        right_layout.addWidget(self.priority_input)

        status_label = QLabel("Status")
        self.status_input = QComboBox()
        self.status_input.addItems(["Not Started", "In Progress", "Completed"])
        right_layout.addWidget(status_label)
        right_layout.addWidget(self.status_input)

        progress_label = QLabel("Progress (%)")
        self.progress_input = QSpinBox()
        self.progress_input.setRange(0, 100)
        self.progress_input.setValue(0)
        right_layout.addWidget(progress_label)
        right_layout.addWidget(self.progress_input)

        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Task")
        self.add_btn.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Update Task")
        self.update_btn.clicked.connect(self.update_task)
        button_layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Delete Task")
        self.delete_btn.clicked.connect(self.delete_task)
        button_layout.addWidget(self.delete_btn)

        self.complete_btn = QPushButton("Mark Complete")
        self.complete_btn.clicked.connect(self.toggle_complete)
        button_layout.addWidget(self.complete_btn)

        right_layout.addLayout(button_layout)

        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)

    def load_tasks(self):
        self.all_tasks = self.db.get_user_tasks(self.user_id)
        self.filter_tasks()

    def filter_tasks(self):
        search_text = self.search_input.text().strip().lower()
        self.task_list.clear()

        filtered_tasks = [
            task for task in self.all_tasks
            if search_text in task[1].lower()
        ]

        for task in filtered_tasks:
            item_text = f"[{'✓' if task[5] == 'Completed' else ' '}] {task[1]} (Due: {task[3]}, P: {task[4]}, S: {task[5]}, Progress: 0%)"  # Placeholder progress
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, task[0])
            self.task_list.addItem(item)

    def task_selected(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        with self.db.conn.cursor() as cur:
            cur.execute("SELECT title, description, due_date, priority, status FROM tasks WHERE id = %s", (task_id,))
            title, desc, due_date, priority, status = cur.fetchone()
            self.title_input.setText(title)
            self.desc_input.setPlainText(desc)
            self.due_date_input.setDate(due_date)
            self.priority_input.setCurrentText(priority)
            self.status_input.setCurrentText(status)
            self.progress_input.setValue(0)  # Placeholder until progress is stored
            self.complete_btn.setText("Mark Incomplete" if self.db.get_task_status(task_id) else "Mark Complete")

    def add_task(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        due_date = self.due_date_input.date().toPyDate()
        priority = self.priority_input.currentText()
        status = self.status_input.currentText()
        progress = self.progress_input.value()

        if not title:
            QMessageBox.warning(self, "Error", "Title cannot be empty")
            return

        # Note: Progress is not yet stored in the database; update db.py first
        self.db.add_task(self.user_id, title, desc, due_date, priority, status)
        self.clear_inputs()
        self.load_tasks()
        self.task_updated.emit()

    def update_task(self):
        current_item = self.task_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Select a task to update")
            return
        task_id = current_item.data(Qt.ItemDataRole.UserRole)
        title = self.title_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        due_date = self.due_date_input.date().toPyDate()
        priority = self.priority_input.currentText()
        status = self.status_input.currentText()
        progress = self.progress_input.value()

        if not title:
            QMessageBox.warning(self, "Error", "Title cannot be empty")
            return

        # Note: Progress is not yet stored in the database; update db.py first
        self.db.update_task(task_id, title, desc, due_date, priority, status)
        self.load_tasks()
        self.task_updated.emit()

    def delete_task(self):
        current_item = self.task_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Select a task to delete")
            return
        task_id = current_item.data(Qt.ItemDataRole.UserRole)
        self.db.delete_task(task_id)
        self.clear_inputs()
        self.load_tasks()
        self.task_updated.emit()

    def toggle_complete(self):
        current_item = self.task_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Select a task to mark")
            return
        task_id = current_item.data(Qt.ItemDataRole.UserRole)
        current_status = self.db.get_task_status(task_id)
        new_status = "Completed" if not current_status else self.status_input.currentText()
        with self.db.conn.cursor() as cur:
            cur.execute("SELECT title, description, due_date, priority, status FROM tasks WHERE id = %s", (task_id,))
            title, desc, due_date, priority, _ = cur.fetchone()
            self.db.update_task(task_id, title, desc, due_date, priority, new_status)
        self.load_tasks()
        self.task_updated.emit()

    def clear_inputs(self):
        self.title_input.clear()
        self.desc_input.clear()
        self.due_date_input.setDate(QDate.currentDate())
        self.priority_input.setCurrentIndex(0)
        self.status_input.setCurrentIndex(0)
        self.progress_input.setValue(0)