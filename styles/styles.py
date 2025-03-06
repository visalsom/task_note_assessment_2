STYLESHEET = """
    QMainWindow {
        background-color: #e0e7ff;
    }
    QWidget {
        background-color: #e0e7ff;
        color: #2d3748;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    /* Navigation Bar */
    QPushButton {
        background-color: #6366f1;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
    }
    QPushButton:hover {
        background-color: #4f46e5;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    QPushButton:pressed {
        background-color: #4338ca;
    }
    QPushButton#logout_btn {
        background-color: #ef4444;
    }
    QPushButton#logout_btn:hover {
        background-color: #dc2626;
    }
    /* Task List Form */
    QTableWidget {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
        color: #2d3748;
        margin: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #f3f4f6;
    }
    QTableWidget::item:selected {
        background-color: #e0e7ff;
        color: #1f2937;
    }
    /* Overdue styling applied programmatically */
    /* Input Fields */
    QLineEdit, QTextEdit, QDateEdit, QComboBox, QSpinBox {
        padding: 8px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-size: 14px;
        background-color: #ffffff;
        color: #2d3748;
        margin: 5px 0;
    }
    QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus, QSpinBox:focus {
        border: 2px solid #6366f1;
        box-shadow: 0 0 5px rgba(99, 102, 241, 0.3);
    }
    /* Labels */
    QLabel {
        color: #1f2937;
        font-size: 14px;
        font-weight: bold;
        margin-top: 10px;
    }
    QLabel#status_label {
        color: #4b5563;
        font-size: 16px;
        font-weight: bold;
        background: linear-gradient(to right, #e0e7ff, #c7d2fe);
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0 5px 0;
    }
    /* Scroll Area */
    QScrollArea {
        background-color: #e0e7ff;
        border: none;
    }
    /* Dialog */
    QDialog {
        background-color: #e0e7ff;
    }
"""