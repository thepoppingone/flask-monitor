# import csv

# with open('test.csv', mode='r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         print(f'\t{row["name"]} maps to {row["url"]}.')
#         line_count += 1
#     print(f'Processed {line_count} lines.')

import secrets
import pandas as pd
import requests
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

def readCSVandTest():
    df= pd.read_csv('test.csv')
    for url in df['url']:
        response= requests.get(url)
        status= response.status_code
        print(status)
        df['Status']=status

scheduler = Scheduler(connection=Redis(host='localhost', port=6379, db=0)) # Get a scheduler for the "default" queue

print(scheduler)

scheduler.schedule(
    scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
    func=readCSVandTest,                     # Function to be queued
    interval=3,                   # Time before the function is called again, in seconds
    repeat=10,                    # Repeat this number of times (None means repeat forever)
)
