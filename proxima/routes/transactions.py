from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Transaction, Membership

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/<int:group_id>/deposit', methods=['POST'])
@jwt_required()
def deposit(group_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get('amount')

    membership = Membership.query.filter_by(user_id=user_id, group_id=group_id).first()
    if not membership:
        return jsonify({"msg": "You are not a member of this group"}), 403

    if not amount or amount <= 0:
        return jsonify({"msg": "Invalid deposit amount"}), 400

    transaction = Transaction(
        group_id=group_id,
        user_id=user_id,
        type='deposit',
        amount=amount
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"msg": "Deposit successful", "transaction_id": transaction.id}), 201

@transactions_bp.route('/<int:group_id>', methods=['GET'])
@jwt_required()
def get_transactions(group_id):
    user_id = get_jwt_identity()

    membership = Membership.query.filter_by(user_id=user_id, group_id=group_id).first()
    if not membership:
        return jsonify({"msg": "You are not a member of this group"}), 403

    transactions = Transaction.query.filter_by(group_id=group_id).all()
    result = []
    for t in transactions:
        result.append({
            "id": t.id,
            "user_id": t.user_id,
            "type": t.type,
            "amount": t.amount,
            "timestamp": t.timestamp.isoformat()
        })

    return jsonify(transactions=result)
