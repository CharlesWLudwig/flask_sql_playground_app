from flask import Flask, abort, send_file, make_response, render_template, url_for, request
import sqlite3
import io
import socket
import pandas as pd
import flask_excel as excel

db_title = 'factbook'
conn = sqlite3.connect(f'{db_title}.db', check_same_thread=False)
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
    return render_template('base.html', db_title=db_title, results=results)

@app.route('/process_query', methods = ['GET', 'POST'])
def process_query():
    if request.method== 'POST':
        global raw_query
        raw_query = request.form["raw_query"]
        global results          
        results = sql_execution(raw_query)      
        results = pd.DataFrame(results)
        str_io = io.StringIO()
    return render_template('process_query.html', str_io=str_io, raw_query=raw_query, db_title=db_title, results=results)

@app.route('/download', methods=['GET', 'POST'])
def download_data(): 
    resp = make_response(results.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
 
if __name__ == '__main__':
    app.debug = True
    app.use_reloader=True
    app.run()