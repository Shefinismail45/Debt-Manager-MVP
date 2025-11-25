from .extensions import db
from datetime import datetime
from decimal import Decimal


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    # 'income' or 'expense'
    kind = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    category = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    occurred_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "kind": self.kind,
            "amount": float(self.amount),
            "category": self.category,
            "description": self.description,
            "occurred_at": self.occurred_at.isoformat()
        }
