from flask import Flask, render_template, request, Response
import requests
from datetime import datetime, timedelta
import json
from flask_cors import cross_origin
import pandas as pd

app = Flask(__name__)


def json_to_csv(data):
    csv_data = []
    for item in data:
        csv_data.append([item["name"], item["age"]])  # CSV 열 추가

    return csv_data


@app.route('/')
@cross_origin(origin='*')
def show():
    hour = int(request.args.get('hours'))

    dateset = hour * 120
    url = f"https://api.thingspeak.com/channels/1999882/feeds.json?&results={dateset}"
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

    graph = {'temp': temp, 'humid': humid, 'sunshine': sunshine, 'time': time_list}

    return json.dumps(graph, ensure_ascii=False)


@app.route('/last')
@cross_origin(origin='*')
def show_last():
    url = "https://api.thingspeak.com/channels/1999882/feeds.json?&results=1"
    response = requests.get(url)
    data = response.json()

    last_data = data['feeds'][0]

    last_data['field1'] = last_data['field1'] + "°C"

    last_data['field2'] = last_data['field2'] + "%"

    last_data['field3'] = last_data['field3'] + "lx"

    last_data['created_at'] = last_data['created_at'].replace('T', ' ').replace('Z', '')

    last_data['created_at'] = datetime.strptime(last_data['created_at'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=9)

    last_data['created_at'] = last_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')

    return json.dumps(last_data, ensure_ascii=False)


@app.route('/landing')
@cross_origin(origin='*')
def landing():
    return render_template('show_graph.html')


@app.route('/show')
@cross_origin(origin='*')
def show_thingspeak():
    return render_template('thingspeak_graph.html')


@app.route('/download')
@cross_origin(origin='*')
def download():
    hours = int(request.args.get('hour'))
    dateset = hours * 120
    url = f"https://api.thingspeak.com/channels/1999882/feeds.json?&results={dateset}"
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

    graph = {'temp': temp, 'humid': humid, 'sunshine': sunshine, 'time': time_list}
    df = pd.DataFrame(graph)

    # CSV로 변환하여 다운로드
    csv_data = df.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=data.csv"
        }
    )


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    main()
