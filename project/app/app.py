from flask import Flask, render_template, request, redirect
import function

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['csvFile']
        datetime_col = int(request.form['datetime_col'])
        data_col = int(request.form['data_col'])
        measurement = request.form['measurement']
        interval = int(request.form['interval'])

        function.process_data(file, datetime_col, data_col, measurement, interval)

        return "OK"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
