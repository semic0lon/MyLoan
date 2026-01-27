from flask import Blueprint, render_template, request, redirect, url_for, abort
from .models import Loan, Payment
from . import db
import subprocess
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

SECRET = "170459"

@main.route("/")
def index():
    loans = Loan.query.order_by(Loan.loan_date.desc()).all()
    return render_template("index.html", loans=loans)

@main.route("/loan/new", methods=["GET", "POST"])
def new_loan():
    if request.method == "POST":
        loan_date = datetime.strptime(request.form["loan_date"], "%Y-%m-%d").date()
        principal = float(request.form["principal"])
        interest_rate = float(request.form["interest_rate"])

        loan = Loan(
            loan_date=loan_date,
            principal=principal,
            interest_rate=interest_rate
        )

        db.session.add(loan)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template("new_loan.html")


@main.route("/manage")
def manage():
    loans = Loan.query.order_by(Loan.loan_date.desc()).all()
    return render_template("manage.html", loans=loans)

@main.route("/loan/<int:loan_id>/edit", methods=["GET", "POST"])
def edit_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)

    if request.method == "POST":
        amount = float(request.form["amount"])
        pay_date = datetime.strptime(request.form["pay_date"], "%Y-%m-%d").date()

        payment = Payment(
            loan_id=loan.id,
            amount=amount,
            pay_date=pay_date
        )

        db.session.add(payment)
        db.session.commit()

        return redirect(url_for("main.edit_loan", loan_id=loan.id))

    status = loan.calculate_status()

    payments = Payment.query.filter_by(loan_id=loan.id).order_by(Payment.pay_date.desc()).all()

    return render_template(
        "edit_loan.html",
        loan=loan,
        status=status,
        payments=payments
    )

@main.route("/loan/<int:loan_id>/delete", methods=["POST"])
def delete_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)

    db.session.delete(loan)
    db.session.commit()

    return redirect(url_for("main.manage"))





@main.route("/deploy")
def deploy():
    open("deploy.trigger", "w").close()
    return "Deploy started"