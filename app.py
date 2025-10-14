from flask import Flask, render_template, request, redirect, url_for
from task_manager import TaskManager

app = Flask(__name__)
task_manager = TaskManager()

@app.route("/")
def index():
    tasks = task_manager.view_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    description = request.form.get("description")
    deadline = request.form.get("deadline") or None
    status = request.form.get("status") or "pending"
    task_manager.add_task(description, deadline, status)
    return redirect(url_for("index"))

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    new_status = request.form.get("status")
    task_manager.update_task(task_id, new_status=new_status)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task_manager.delete_task(task_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
