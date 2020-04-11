# coding utf-8
import requests
import subprocess
import schedule
import time

def job():
    response = requests.get("http://127.0.0.1:5000")
    cmd = 'seikasay -cid 2000 -t "{}"'.format(response.json()["args"]["message"] )
    returncode = subprocess.run(cmd,shell=True)

if __name__== '__main__':
    schedule.every(1).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)