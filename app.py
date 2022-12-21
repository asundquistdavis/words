from flask import Flask, render_template

app = Flask(__name__)

@app.route('/scrape')
def scrape_action():
    pass

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run