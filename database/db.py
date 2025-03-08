import psycopg2
import hashlib

try:
    import config
except ImportError:
    print("config.py not found. Please create it based on config.example.py with your database credentials.")
    raise


class Database:
    def __init__(self):
        # Retrieve credentials from config.py
        self.db_name = config.DB_NAME
        self.db_user = config.DB_USER
        self.db_password = config.DB_PASSWORD
        self.db_host = config.DB_HOST
        self.db_port = config.DB_PORT

        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            raise

        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            # Create users table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(64) NOT NULL
                )
            """)

            # Create tasks table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    due_date DATE,
                    priority VARCHAR(20),
                    status VARCHAR(20),
                    progress INTEGER DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Check if the progress column exists in the tasks table
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'tasks' AND column_name = 'progress'
            """)
            if not cur.fetchone():
                # Add the progress column if it doesn't exist
                cur.execute("""
                    ALTER TABLE tasks 
                    ADD COLUMN progress INTEGER DEFAULT 0
                """)
                print("Added 'progress' column to tasks table.")

            self.conn.commit()

    def verify_user(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s AND password = %s",
                       (username, hashed_pw))
            result = cur.fetchone()
            return result[0] if result else None

    def register_user(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        try:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                          (username, hashed_pw))
                self.conn.commit()
                return cur.fetchone()[0]
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return None

    def get_user_tasks(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, description, due_date, priority, status, progress
                FROM tasks WHERE user_id = %s
            """, (user_id,))
            return cur.fetchall()

    def add_task(self, user_id, title, desc, due_date, priority, status, progress=0):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tasks (user_id, title, description, due_date, priority, status, progress)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (user_id, title, desc, due_date, priority, status, progress))
            self.conn.commit()

    def update_task(self, task_id, title, desc, due_date, priority, status, progress):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE tasks
                SET title = %s, description = %s, due_date = %s, priority = %s, status = %s, progress = %s
                WHERE id = %s
            """, (title, desc, due_date, priority, status, progress, task_id))
            self.conn.commit()

    def delete_task(self, task_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.conn.commit()

    def get_task_status(self, task_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT status FROM tasks WHERE id = %s", (task_id,))
            status = cur.fetchone()
            return status[0] == "Completed" if status else False