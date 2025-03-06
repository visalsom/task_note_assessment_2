# Python Project Setup Guide

Follow these steps to set up the project, create a virtual environment, install dependencies, and run the application.

---

## 2. Create a Virtual Environment

A virtual environment ensures that project dependencies are isolated. To create one:

- **On macOS/Linux**:
  1. Run the command:
     ```bash
     python -m venv venv
     ```
  2. Activate the virtual environment:
     ```bash
     source venv/bin/activate
     ```

- **On Windows**:
  1. Run the command:
     ```bash
     python -m venv venv
     ```
  2. Activate the virtual environment:
     ```bash
     venv\Scripts\activate
     ```

When the virtual environment is activated, your terminal prompt will display `(venv)`.

---

## 3. Install Dependencies

Once the virtual environment is active, install the required dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
