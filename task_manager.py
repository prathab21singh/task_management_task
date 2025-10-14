import sqlite3 as s
from datetime import datetime

class TaskManager:
    def __init__(self,db_name="task.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):

        try:
            c = s.connect(self.db_name)
            cur = c.cursor()
            query = """
                    CREATE TABLE IF NOT EXISTS tasks(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        deadline TEXT,
                        status TEXT CHECK(status IN ('pending', 'completed')))
                    """
            cur.execute(query)
            c.commit()
        except s.Error as err:
            print(f'Database Error: {err}')

        c.close()

    def add_task(self, description, deadline, status="pending"):

        try:
            if not description.strip():
                raise ValueError("Description cannot be empty")

            if deadline:
                try:
                    datetime.strptime(deadline, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Invalid deadline format, Use (YYY-MM-DD)")

            if status not in ["pending", "completed"]:
                raise ValueError("Invalid Status. Choose 'pending' or 'complete'")

            c = s.connect(self.db_name)
            cur = c.cursor()
            cur.execute("INSERT INTO tasks (description, deadline, status) VALUES (?, ?, ?)", (description, deadline, status))
            c.commit()
            print("Task added successfully")
        except s.Error as err:
            print(f'Found Error while adding task: {err}')

        c.close()

    # Added sort task for status
    def view_tasks(self):
        try:
            c = s.connect(self.db_name)
            cur = c.cursor()
            query = """SELECT * FROM tasks
                        ORDER BY CASE
                                WHEN status='pending' THEN 1
                                WHEN status='completed' THEN 2
                                END
                    """
            cur.execute(query)
            tasks = cur.fetchall()
            c.close()
            return tasks
        except s.Error as err:
            print(f"Error fetching tasks: {err}")

    def view_tasks_by_status(self,status):
        try:
            c = s.connect(self.db_name)
            cur = c.cursor()
            if status not in ['pending','completed']:
                raise ValueError("Invalid Status. Choose 'pending' or 'complete'")

            cur.execute("SELECT * FROM tasks WHERE status = ?", (status,))
            tasks = cur.fetchall()
            c.close()

            if tasks:
                return tasks
            else:
                raise ValueError(f"No {status} status are found")
        except s.Error as err:
            print(f"Error fetching task by status: {err}")

    def update_task(self, task_id, new_description=None, new_status=None):

        try:
            c = s.connect(self.db_name)
            cur = c.cursor()

            if new_description:
                cur.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
            if new_status:
                cur.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
            c.commit()
            print("Task updated successfully!")
        except s.Error as err:
            print(f"Error updaing task: {err}")

        c.close()

    def delete_task(self,task_id):

        try:
            c = s.connect(self.db_name)
            cur = c.cursor()
            cur.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
            c.commit()
            print("Task deleted sucessfully")

            if cur.rowcount > 0:
                print("Task deleted successfully")
            else:
                print("No task found with the given ID")

        except s.Error as err:
            print(f'Error in deleting task: {err}')

        c.close()


    def search_tasks_by_description(self, keyword):
        try:
            conn = s.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE description LIKE ?", (f"%{keyword}%",))
            tasks = cursor.fetchall()
            conn.close()
            if tasks:
                return tasks
            else:
                raise ValueError(f"No task with keyword {keyword}")
        except s.Error as err:
            print(f"Error searching tasks: {err}")
