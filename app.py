from flask import Flask, render_template, request
from selenium_final import scrape_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    origin_zip = request.form['originZip']
    destination_zip = request.form['destinationZip']
    length = request.form['dimensionX']
    width = request.form['dimensionY']
    height = request.form['dimensionZ']
    weight_pounds = request.form['weightPounds']
    weight_ounces = request.form['weightOunces']
    results = scrape_data(origin_zip, destination_zip, length, width, height, weight_pounds, weight_ounces)
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
