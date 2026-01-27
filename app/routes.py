from flask import Blueprint, render_template, request, redirect, url_for, abort
from .models import Loan
from . import db
import subprocess

main = Blueprint('main', __name__)

SECRET = "170459"

@main.route("/")
def home():
    loans = Loan.query.all()
    return render_template("index.html", loans=loans)

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]

        loan = Loan(name=name, amount=amount)
        db.session.add(loan)
        db.session.commit()

        return redirect(url_for("main.home"))

    return render_template("add.html")
@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    loan = Loan.query.get_or_404(id)

    if request.method == "POST":
        loan.name = request.form["name"]
        loan.amount = request.form["amount"]
        db.session.commit()
        return redirect(url_for("main.home"))

    return render_template("edit.html", loan=loan)


@main.route("/delete/<int:id>")
def delete(id):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    return redirect(url_for("main.home"))






@main.route("/deploy")
def deploy():
    open("deploy.trigger", "w").close()
    return "Deploy started"