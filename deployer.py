import subprocess
import os

BASE_DIR = r"C:\MyLoan"

def run(cmd):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    os.chdir(BASE_DIR)

    print("STEP 1: git pull")
    run("git pull")

    print("STEP 2: install requirements")
    run(r"venv\Scripts\pip install -r requirements.txt")

    print("STEP 3: migrate database")
    run(r"venv\Scripts\flask db upgrade")

    print("STEP 4: restart service")
    run("nssm restart Loan")

    print("DEPLOY DONE")

if __name__ == "__main__":
    main()
