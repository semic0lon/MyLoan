from flask import Blueprint, render_template, request, abort
import subprocess

main = Blueprint('main', __name__)

SECRET = "mysecret123"

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/deploy")
def deploy():
    if request.args.get("key") != SECRET:
        abort(403)

    subprocess.run(
        ["git", "pull"],
        cwd=r"C:\MyLoan",
        capture_output=True,
        text=True
    )

    subprocess.Popen(
        ["nssm", "restart", "MyLoanFlask"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    return "Deploy & Restart สำเร็จ"