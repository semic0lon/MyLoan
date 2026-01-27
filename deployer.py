import os
import time
import subprocess
import traceback

BASE = r"C:\MyLoan"
TRIGGER = os.path.join(BASE, "deploy.trigger")
PYTHON = r"C:\MyLoan\venv\Scripts\python.exe"

def run(cmd):
    print(f"RUN: {cmd}")
    subprocess.call(cmd, cwd=BASE, shell=True)

while True:
    try:
        if os.path.exists(TRIGGER):
            print("Deploy triggered")
            os.remove(TRIGGER)

            run("git pull")
            run(f'"{PYTHON}" -m pip install -r requirements.txt')
            run(f'"{PYTHON}" -m flask db upgrade')
            run("nssm restart Loan")

        time.sleep(5)

    except Exception:
        with open(os.path.join(BASE, "deployer_error.log"), "a") as f:
            f.write(traceback.format_exc())
        time.sleep(5)
