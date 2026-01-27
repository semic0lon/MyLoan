import os
from flask import request, abort
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "testing deploy route 2"












DEPLOY_KEY = "170459"  
@app.route("/deploy")
def deploy():
    key = request.args.get("key")

    if key != DEPLOY_KEY:
        abort(403)

    # ดึงโค้ดล่าสุด
    os.system("cd C:\\MyLoan && git pull")

    # สั่งให้ Task Flask รันใหม่
    os.system('schtasks /end /tn "MyLoan Flask Server"')
    os.system('schtasks /run /tn "MyLoan Flask Server"')

    return "Deploy success!"