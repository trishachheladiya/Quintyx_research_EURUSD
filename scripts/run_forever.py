import subprocess
import time
from datetime import datetime

last_hour = None

while True:

    now = datetime.now()

    if now.minute == 1 and now.hour != last_hour:

        print("\nRunning after H1 candle close...")

        subprocess.run([
            r"C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe",
            r"C:\Users\DELL\Desktop\Quintyx_Research\scripts\live_signal.py"
        ])

        last_hour = now.hour

    time.sleep(5)