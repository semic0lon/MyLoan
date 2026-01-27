import os
from flask import request, abort
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "testing 7"












DEPLOY_KEY = "170459"  
@app.route("/deploy")
def deploy():
    key = request.args.get("key")
    if key != DEPLOY_KEY:
        abort(403)

    os.system("cd C:\\MyLoan && git pull")

    return "Pulled. Please wait 10 seconds..."