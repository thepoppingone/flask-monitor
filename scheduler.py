from base64 import urlsafe_b64decode
from flask import Flask, jsonify, request, redirect, abort, render_template_string
import time
import threading
from unittest import skip
import requests
import pandas as pd
import schedule
from datetime import datetime
import json
from json import JSONEncoder

app = Flask(__name__)


class StatusRecord(dict):
  def __init__(self, timestamp, status):
    dict.__init__(self, timestamp=timestamp, status=status)

class StatusRecordEncoder(JSONEncoder):
  def default(self, o):
    return o.__dict__

url_status_records = {}

def saveStatus(url, status):
    print(status)
    now = datetime.now()
    sr = StatusRecord(now,status)
    if url not in url_status_records:
        url_status_records[url] = []
        url_status_records[url].insert(0,sr)
    else:
        url_status_records[url] = url_status_records[url][0:6] 
        url_status_records[url].insert(0,sr)

def task():
    df= pd.read_csv('test.csv')
    for url in df['url']:
        try: 
            response= requests.get(url)
            status= response.status_code
            saveStatus(url, status)
        except requests.exceptions.Timeout:
            print('to')
        # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            print('redirect')
        # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
        # catastrophic error. bail
            print("404")
            status=404
            saveStatus(url, status)
            continue
            raise SystemExit(e)      
        
    print("PULSE END")


def scheduleFunc():
    while 1:
        schedule.run_pending()
        time.sleep(1)

# makes our logic non blocking
thread = threading.Thread(target=scheduleFunc)
thread.start()
schedule.every(2).seconds.do(task)

print("no block")

@app.route('/', methods=['GET'])
def index():
    # for url in url_status_records:
    # encode test
    # print(StatusRecordEncoder().encode(url_status_records['url'][0]))
    #statusJSONDATA = json.dumps(url_status_records, indent=4 , cls=StatusRecordEncoder)
    # for url in url_status_records:
        # print(url)
    # return jsonify(url_status_records)
    return render_template_string('''
    <table>
            <tr>
                <td> URL </td>
                <td> Status Now </td>
                <td> Status 10m ago </td>
                <td> Status 20m ago </td>
                <td> Status 30m ago </td>
                <td> Status 40m ago </td>
                <td> Status 50m ago </td>
                <td> Status 60m ago </td>
            </tr>
            {% for url in url_status_records %}
            <tr>
                <td> {{ url }} </td>

                {% for record in url_status_records[url] %}
                <td> {{ record['status'] }} </td>
                {% endfor %}
            </tr>

            {% endfor %}

    </table>
''', url_status_records=url_status_records)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)