from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"homework": []}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)
    

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', homework=data["homework"])


@app.route('/add', methods=['POST'])
def add_homework():
    lesson = request.form['lesson']
    task = request.form['task']
    deadline= request.form['deadline']
    new_hw = {
        "lesson": lesson,
        "task": task,
        "deadline": deadline,
        "completed": False
    }
    data = load_data()
    data["homework"].append(new_hw)
    save_data(data)
    return redirect(url_for('index'))

@app.route('/complete/<int:index>')
def complete_homework(index):
    data = load_data()
    if 0 <= index < len(data["homework"]):
        data["homework"][index]["completed"] = True
        save_data(data)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_homework(index):
    data = load_data()
    if 0 <= index < len(data["homework"]):
        data["homework"].pop(index)
        save_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__' :
    app.run(debug=True)