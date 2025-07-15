from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB if not exists
def init_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY, name TEXT, deadline TEXT, priority TEXT, status TEXT)''')
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    tasks = conn.execute("SELECT * FROM tasks ORDER BY deadline").fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        deadline = request.form['deadline']
        priority = request.form['priority']
        conn = sqlite3.connect('tasks.db')
        conn.execute("INSERT INTO tasks (name, deadline, priority, status) VALUES (?, ?, ?, 'Pending')",
                     (name, deadline, priority))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_task.html')

@app.route('/complete/<int:task_id>')
def complete(task_id):
    conn = sqlite3.connect('tasks.db')
    conn.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('tasks.db')
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
