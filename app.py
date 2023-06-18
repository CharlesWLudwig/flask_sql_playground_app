from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/process_query', methods = ['GET', 'POST'])
def process_query():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=True)