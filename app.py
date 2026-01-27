import os
import subprocess
from flask import request, abort
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "testing 11"












DEPLOY_KEY = "170459"  
@app.route("/deploy")
def deploy():
    # 1) git pull
    subprocess.run(
        ["git", "pull"],
        cwd=r"C:\MyLoan",
        capture_output=True,
        text=True
    )

    # 2) restart service แบบที่ไม่ค้าง
    subprocess.Popen(
        ["nssm", "restart", "MyLoanFlask"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    return "Deploy & Restart Service สำเร็จ"