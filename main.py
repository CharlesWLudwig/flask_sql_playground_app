from flask import Flask, render_template, url_for, request
import sqlite3
import pandas as pd

conn = sqlite3.connect('factbook.db', check_same_thread=False)
c = conn.cursor()

def sql_execution(raw_query):
    c.execute(raw_query)
    data = c.fetchall()
    # pandas
    return data

app = Flask(__name__)

@app.route("/")
def index():
    results = pd.DataFrame([])
    return render_template('index.html', results=results)

@app.route('/process_query', methods = ['GET', 'POST'])
def process_query():
    if request.method== 'POST':
        raw_query = request.form["raw_query"]
        results = sql_execution(raw_query)
        results = pd.DataFrame(results)
    return render_template('index.html', raw_query=raw_query, results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5002, use_reloader=True)