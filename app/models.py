from . import db
from datetime import date
from decimal import Decimal, ROUND_HALF_UP


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.Date, nullable=False)

    # DB ยังเป็น Float ได้ แต่ตอนคำนวณต้องแปลง
    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)

    payments = db.relationship(
        'Payment',
        backref='loan',
        lazy=True,
        cascade="all, delete"
    )

    def calculate_status(self):
        start_date = self.loan_date
        last_date = start_date

        # ✅ แปลงเป็น Decimal ตั้งแต่ต้น
        current_principal = Decimal(str(self.principal))
        interest_rate = Decimal(str(self.interest_rate))

        accrued_interest = Decimal("0.00")

        payments = sorted(self.payments, key=lambda p: p.pay_date)

        for p in payments:
            days = (p.pay_date - last_date).days

            if days > 0:
                daily_rate = (
                    current_principal * interest_rate / Decimal(100) / Decimal(365)
                )
                interest = (Decimal(days) * daily_rate)
                accrued_interest += interest

            payment_left = Decimal(str(p.amount))

            # ตัดดอกก่อน
            if payment_left >= accrued_interest:
                payment_left -= accrued_interest
                accrued_interest = Decimal("0.00")
                current_principal -= payment_left
            else:
                accrued_interest -= payment_left

            last_date = p.pay_date

        # คิดดอกจากวันล่าสุดถึงวันนี้
        days = (date.today() - last_date).days
        daily_rate = (
            current_principal * interest_rate / Decimal(100) / Decimal(365)
        ).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

        if days > 0:
            accrued_interest += Decimal(days) * daily_rate

        return {
            "principal": current_principal.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP),
            "interest": accrued_interest.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP),
            "daily_interest": daily_rate,
            "start_date": start_date
        }


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    pay_date = db.Column(db.Date, nullable=False, default=date.today)
    amount = db.Column(db.Float, nullable=False)

class Loan2(db.Model):
    __tablename__ = "loan2"   # ชื่อตารางใหม่

    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.Date, nullable=False)

    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)

    payments = db.relationship(
        'Payment2',
        backref='loan',
        lazy=True,
        cascade="all, delete"
    )

    def calculate_status(self):
        start_date = self.loan_date
        last_date = start_date

        from decimal import Decimal, ROUND_HALF_UP
        from datetime import date

        current_principal = Decimal(str(self.principal))
        interest_rate = Decimal(str(self.interest_rate))

        accrued_interest = Decimal("0.00")

        payments = sorted(self.payments, key=lambda p: p.pay_date)

        for p in payments:
            days = (p.pay_date - last_date).days

            if days > 0:
                daily_rate = (
                    current_principal * interest_rate / Decimal(100) / Decimal(365)
                )
                interest = Decimal(days) * daily_rate
                accrued_interest += interest

            payment_left = Decimal(str(p.amount))

            if payment_left >= accrued_interest:
                payment_left -= accrued_interest
                accrued_interest = Decimal("0.00")
                current_principal -= payment_left
            else:
                accrued_interest -= payment_left

            last_date = p.pay_date

        days = (date.today() - last_date).days

        daily_rate = (
            current_principal * interest_rate / Decimal(100) / Decimal(365)
        ).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

        if days > 0:
            accrued_interest += Decimal(days) * daily_rate

        return {
            "principal": current_principal.quantize(Decimal("0.00")),
            "interest": accrued_interest.quantize(Decimal("0.00")),
            "daily_interest": daily_rate,
            "start_date": start_date
        }


class Payment2(db.Model):
    __tablename__ = "payment2"

    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan2.id'), nullable=False)

    pay_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
