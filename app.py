from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import subprocess

app = Flask(__name__)

def calculate_sum(num1, num2):
    return num1 + num2

def check_duplicate(num1, num2):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM calculations WHERE num1=? AND num2=?', (num1, num2))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])

    if not check_duplicate(num1, num2):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS calculations (num1 INTEGER, num2 INTEGER, result INTEGER)')
        cursor.execute('INSERT INTO calculations (num1, num2) VALUES (?, ?)', (num1, num2))
        conn.commit()
        conn.close()

    return redirect(url_for('show_results'))

@app.route('/calculate_sum')
def calculate_sum_route():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT num1, num2 FROM calculations')
    calculations = cursor.fetchall()
    conn.close()

    results = [calculate_sum(num1, num2) for num1, num2 in calculations]
    return render_template('result.html', calculations=calculations, results=results)

@app.route('/calculate_sub')
def calculate_sub():
    # Call sub.py script using subprocess
    subprocess.call(["python", "sub.py"])
    return "Subtraction calculation completed."

@app.route('/results')
def show_results():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT num1, num2 FROM calculations')
    calculations = cursor.fetchall()
    conn.close()

    return render_template('result.html', calculations=calculations)

if __name__ == '__main__':
    app.run(debug=True)
