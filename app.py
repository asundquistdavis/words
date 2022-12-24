from flask import Flask, render_template, jsonify
from scrape import get_data

app = Flask(__name__)

@app.route('/scrape')
def scrape_action():
    pass

@app.route('/')
def about_page():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/api/data')
def data_call():
    return jsonify(get_data())

if __name__ == '__main__':
    app.run(debug=True)