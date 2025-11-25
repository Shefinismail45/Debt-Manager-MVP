from flask import Blueprint, jsonify, request
from .models import Transaction
from .extensions import db
from datetime import datetime

# Create blueprint FIRST
bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return jsonify({"status": "ok", "app": "personal-finance-mvp"})


@bp.post("/transactions")
def create_transaction():
    data = request.get_json() or {}
    kind = data.get("kind")
    amount = data.get("amount")

    if kind not in ("income", "expense") or amount is None:
        return jsonify({"error": "invalid payload"}), 400

    t = Transaction(
        kind=kind,
        amount=amount,
        category=data.get("category"),
        description=data.get("description"),
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@bp.get("/transactions")
def list_transactions():
    q = Transaction.query

    kind = request.args.get("kind")
    if kind in ("income", "expense"):
        q = q.filter(Transaction.kind == kind)

    start = request.args.get("start")
    end = request.args.get("end")

    if start:
        try:
            s_dt = datetime.fromisoformat(start)
            q = q.filter(Transaction.occurred_at >= s_dt)
        except:
            return jsonify({"error": "invalid start date"}), 400

    if end:
        try:
            e_dt = datetime.fromisoformat(end)
            q = q.filter(Transaction.occurred_at <= e_dt)
        except:
            return jsonify({"error": "invalid end date"}), 400

    items = q.order_by(Transaction.occurred_at.desc()).all()
    return jsonify([i.to_dict() for i in items])


@bp.get("/summary")
def summary():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    q = Transaction.query

    if year and month:
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        q = q.filter(Transaction.occurred_at >= start,
                     Transaction.occurred_at < end)

    elif year:
        start = datetime(year, 1, 1)
        end = datetime(year + 1, 1, 1)
        q = q.filter(Transaction.occurred_at >= start,
                     Transaction.occurred_at < end)

    records = q.all()

    total_income = sum(float(r.amount) for r in records if r.kind == "income")
    total_expense = sum(float(r.amount)
                        for r in records if r.kind == "expense")
    balance = total_income - total_expense

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "year": year,
        "month": month,
    })
