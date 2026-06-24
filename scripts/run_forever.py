import subprocess
import time

while True:

    print("\n======================")
    print("RUNNING QUINTYX")
    print("======================")

    subprocess.run([
        r"C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe",
        r"C:\Users\DELL\Desktop\Quintyx_Research\scripts\live_signal.py"
    ])

    print("\nSleeping for 1 hour...")
    time.sleep(3600)