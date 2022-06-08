import time
import threading
import requests
import pandas as pd

def task():
    df= pd.read_csv('test.csv')
    for url in df['url']:
        response= requests.get(url)
        status= response.status_code
        df['StatusNow']=status
    print(df)


def schedule():
    while 1:
        task()
        time.sleep(3)

# makes our logic non blocking
thread = threading.Thread(target=schedule)
thread.start()