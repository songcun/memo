from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')

tasks = []

# 汎用的なデータベースにつなぐ関数
def get_db():
    db = sqlite3.connect('memo.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        try:
            db = get_db()

            # with db:
            #     with app.open_resource('schema.sql', mode='r') as f:
            #         db.executescript(f.read())
        finally:
            db.close()
init_db()


@app.route('/', methods=['GET'])
def index():
    try:
        db = get_db()

        with db:
            # tasks = db.execute('SELECT * FROM tasks ').fetchall()
            tasks = db.execute('SELECT * FROM tasks LEFT JOIN categories on tasks.category_id = categories.id').fetchall()
            categories = db.execute('SELECT * FROM categories').fetchall()

        return render_template('index.html', tasks=tasks, categories=categories)
    finally:
        db.close()


@app.route('/', methods=['POST'])
def create():
    task = request.form['task']
    category_id = int(request.form['category_id'])

    try:
        db = get_db()
        with db:
            db.execute('INSERT INTO tasks (task, category_id) VALUES (?, ?)', (task, category_id,))

        return redirect('/')
    finally:
        db.close()


@app.route('/finish', methods=['POST'])
def finish():
    try:
        db = get_db()
        task_id = int(request.form['task_id'])

        with db:
            db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))  # タプルにするためにカンマが必要
        
        return redirect('/')
    finally:
        db.close()

@app.route('/edit', methods=['POST'])
def edit():
    try:
        db = get_db()
        task_id = int(request.form['task_id'])
        task = request.form['task']
        category_id = int(request.form['category_id'])

        with db:
            db.execute('UPDATE tasks SET task = ?, category_id = ? WHERE id = ?', (task, category_id, task_id, ))
        return redirect('/')
    finally:
        db.close()
