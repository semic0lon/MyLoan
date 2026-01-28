from . import db
from datetime import date, timedelta


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.Date, nullable=False)
    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)

    payments = db.relationship(
        'Payment',
        backref='loan',
        lazy=True,
        cascade="all, delete"
    )

    # ===== method คำนวณสถานะเงินจริง (คิดดอกตั้งแต่วันกู้) =====
    def calculate_status(self):
        start_date = self.loan_date
        current_principal = self.principal
        accrued_interest = 0.0
        last_date = start_date

        payments = sorted(self.payments, key=lambda p: p.pay_date)

        for p in payments:
            days = (p.pay_date - last_date).days

            if days > 0:
                daily_rate = (current_principal * (self.interest_rate / 100)) / 365
                interest = days * daily_rate
                accrued_interest += interest

            payment_left = p.amount

            # ตัดดอกก่อน
            if payment_left >= accrued_interest:
                payment_left -= accrued_interest
                accrued_interest = 0
                current_principal -= payment_left
            else:
                accrued_interest -= payment_left

            last_date = p.pay_date

        # คิดดอกจากวันล่าสุดถึงวันนี้
        days = (date.today() - last_date).days
        daily_rate = (current_principal * (self.interest_rate / 100)) / 365

        if days > 0:
            accrued_interest += days * daily_rate

        return {
            "principal": round(current_principal, 2),
            "interest": round(accrued_interest, 2),
            "daily_interest": round(daily_rate, 2),
            "start_date": start_date
        }


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    pay_date = db.Column(db.Date, nullable=False, default=date.today)
    amount = db.Column(db.Float, nullable=False)
