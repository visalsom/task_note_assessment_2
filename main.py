import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import TaskManager

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskManager()
    sys.exit(app.exec())