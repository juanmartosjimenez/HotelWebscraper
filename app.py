from flask import Flask, render_template, request, send_from_directory

from bookingscrape import booking
from processhotellist import initialize
from tripadvisorscrape import tripadvisor

app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def my_form_post():
    location = request.form['location']
    datesin = str(request.form['indate-y'] + "-" + request.form['indate-m'] + "-" + request.form['indate-d'])
    datesout = str(request.form['outdate-y'] + "-" + request.form['outdate-m'] + "-" + request.form['outdate-d'])

    # path1 = 'images/carcabueybooking.png'
    # path2 = 'images/carcabueytripadvisor.png'
    print("Ok....")

    # booking(location, datesin, datesout)
    bookingpathname = "static/images/" + location + "booking" + ".png"
    # tripadvisor(location, datesin, datesout)
    tripadvisorpathname = "static/images/" + location + "tripadvisor" + ".png"
    path1 = bookingpathname.replace("static", "")
    path2 = tripadvisorpathname.replace("static", "")
    initialize('csvfiles/madridbooking.csv', "booking", "madridbooking", 1)
    initialize('csvfiles/madridtripadvisor.csv', "tripadvisor", "madridtripadvisor", 2)
    return render_template('result.html', location=location, indate=datesin, outdate=datesout, path1=path1, path2=path2)


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('images', path)


if __name__ == '__main__':
    app.run(debug=True)
