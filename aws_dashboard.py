from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)


@app.route('/')
def show():
    url = "https://api.thingspeak.com/channels/1999882/feeds.json?&results=4000"
    response = requests.get(url)
    data = response.json()

    temp = [x['field1'] for x in data['feeds']][::5]
    humid = [x['field2'] for x in data['feeds']][::5]
    sunshine = [x['field3'] for x in data['feeds']][::5]
    # wind_dir = [x['field4'] for x in data['feeds']]
    # wind_speed = [x['field5'] for x in data['feeds']]

    time = [x['created_at'].replace('T', ' ').replace('Z', '') for x in data['feeds']]

    date = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') + timedelta(hours=9) for x in time]

    time_list = [x.strftime('%Y-%m-%d %H:%M:%S') for x in date][::5]

    graph = {'temp': temp, 'humid': humid, 'sunshine': sunshine,'time': time_list}

    return json.dumps(graph, ensure_ascii=False)


@app.route('/landing')
def landing():
    return render_template('show_graph.html')


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    main()
