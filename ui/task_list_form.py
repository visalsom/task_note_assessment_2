from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QScrollArea, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QDate
import datetime

class TaskListForm(QWidget):
    def __init__(self, user_id, db):
        super().__init__()
        self.user_id = user_id
        self.db = db
        self.initUI()
        self.load_tasks()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Scroll area for grouped tasks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)  # Allows the content to resize with the scroll area
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Group tasks by status using tables
        self.not_started_label = QLabel("Not Started")
        self.not_started_label.setObjectName("status_label")
        self.not_started_table = QTableWidget()
        self.in_progress_label = QLabel("In Progress")
        self.in_progress_label.setObjectName("status_label")
        self.in_progress_table = QTableWidget()
        self.completed_label = QLabel("Completed")
        self.completed_label.setObjectName("status_label")
        self.completed_table = QTableWidget()

        # Set up table headers and responsive sizing
        headers = ["ID", "Title", "Description", "Due Date", "Priority", "Status", "Progress"]
        for table in [self.not_started_table, self.in_progress_table, self.completed_table]:
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.setWordWrap(True)  # Enable word wrap for text
            # Set stretch mode for all columns except the last one, which will take remaining space
            for i in range(len(headers) - 1):
                table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(len(headers) - 1, QHeaderView.ResizeMode.Stretch)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Add widgets to layout
        scroll_layout.addWidget(self.not_started_label)
        scroll_layout.addWidget(self.not_started_table)
        scroll_layout.addWidget(self.in_progress_label)
        scroll_layout.addWidget(self.in_progress_table)
        scroll_layout.addWidget(self.completed_label)
        scroll_layout.addWidget(self.completed_table)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def load_tasks(self):
        # Clear tables
        self.not_started_table.setRowCount(0)
        self.in_progress_table.setRowCount(0)
        self.completed_table.setRowCount(0)

        # Fetch tasks from the database
        tasks = self.db.get_user_tasks(self.user_id)

        # Structured table representation (for reference or export)
        table_data = {
            "table_name": "tasks",
            "records": []
        }

        today = QDate.currentDate()
        for task in tasks:
            try:
                task_id, title, description, due_date, priority, status, progress = task

                # Create a record dictionary for the table
                record = {
                    "id": task_id,
                    "title": title,
                    "description": description or "N/A",
                    "due_date": str(due_date),
                    "priority": priority,
                    "status": status,
                    "progress": progress
                }
                table_data["records"].append(record)

                # Convert datetime.date to QDate for overdue check
                due_date_qdate = QDate(due_date.year, due_date.month, due_date.day)
                is_overdue = due_date_qdate < today and status != "Completed"

                # Determine which table to add the task to
                if status == "Not Started":
                    table = self.not_started_table
                elif status == "In Progress":
                    table = self.in_progress_table
                else:  # status == "Completed"
                    table = self.completed_table

                # Add a new row to the table
                row_position = table.rowCount()
                table.insertRow(row_position)

                # Populate the row with task details
                items = [
                    QTableWidgetItem(str(task_id)),
                    QTableWidgetItem(title),
                    QTableWidgetItem(description or "N/A"),
                    QTableWidgetItem(str(due_date)),
                    QTableWidgetItem(priority),
                    QTableWidgetItem(status),
                    QTableWidgetItem(f"{progress}%")
                ]
                for col, item in enumerate(items):
                    table.setItem(row_position, col, item)
                    # Ensure the item can handle long text
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

                # Apply overdue styling
                if is_overdue:
                    for col in range(table.columnCount()):
                        item = table.item(row_position, col)
                        if item:
                            item.setBackground(Qt.GlobalColor.red)

            except Exception as e:
                print(f"Error processing task: {task}, Error: {e}")

        # Print the structured table data for debugging
        print("Structured Table Data:")
        print(f"Table Name: {table_data['table_name']}")
        print("Records:")
        for record in table_data["records"]:
            print(record)