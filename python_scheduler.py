import schedule
import time
from script import run_stock_job  # your existing script
from datetime import datetime

# Change this to the interval you want (in minutes)
SCHEDULER_INTERVAL_MINUTES = 5

def timestamp_job():
    print("Scheduler checked at:", datetime.now())

# Print timestamp every minute (optional)
schedule.every().minute.do(timestamp_job)

# Schedule your ticker job safely
schedule.every(SCHEDULER_INTERVAL_MINUTES).minutes.do(run_stock_job)

print(f"Scheduler started. run_stock_job will run every {SCHEDULER_INTERVAL_MINUTES} minutes.")

while True:
    schedule.run_pending()
    time.sleep(1)  # checks every second for pending jobs
