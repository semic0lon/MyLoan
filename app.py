import os
from flask import request, abort
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "testing 9"












DEPLOY_KEY = "170459"  
@app.route("/deploy")
def deploy():
    key = request.args.get("key")
    if key != DEPLOY_KEY:
        abort(403)

    os.system("cd C:\\MyLoan && git pull")

    # สั่งหยุด task อย่างเดียว
    os.system('schtasks /end /tn "MyLoan Flask Server"')

    return "Pulled. Service will restart within 1 minute."