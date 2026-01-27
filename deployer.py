import os
import time
import subprocess

TRIGGER = r"C:\MyLoan\deploy.trigger"
BASE = r"C:\MyLoan"

while True:
    if os.path.exists(TRIGGER):
        os.remove(TRIGGER)

        subprocess.call("git pull", cwd=BASE, shell=True)
        subprocess.call(r"venv\Scripts\python -m pip install -r requirements.txt", cwd=BASE, shell=True)
        subprocess.call(r"venv\Scripts\python -m flask db upgrade", cwd=BASE, shell=True)

        subprocess.call("nssm restart Loan", shell=True)

    time.sleep(5)
