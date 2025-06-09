from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Group, Membership, User

groups_bp = Blueprint('groups', __name__)

# Create a new group
@groups_bp.route('/', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()  # Get data from the request
    name = data.get('name')
    description = data.get('description')
    print('des',description)
    user_id = get_jwt_identity()  # Get user from JWT token

    # Validate the presence of name and description
    if not name or not description:
        return jsonify({"msg": "Group name and description are required"}), 400

    # Check if 'name' and 'description' are strings
    if not isinstance(name, str):
        return jsonify({"msg": "Group name must be a string"}), 400

    if not isinstance(description, str):
        return jsonify({"msg": "Group description must be a string"}), 400

    # Create new group
    group = Group(name=name, description=description, created_by=user_id)
    db.session.add(group)
    db.session.commit()

    # Add the creator as the admin member
    membership = Membership(user_id=user_id, group_id=group.id, role='admin')
    db.session.add(membership)
    db.session.commit()

    return jsonify({"msg": "Group created successfully",}), 201

# List all groups for the logged-in user
@groups_bp.route('/', methods=['GET'])
@jwt_required()
def list_groups():
    user_id = get_jwt_identity()  # Get user ID from JWT token

    # Fetch all groups where the current user is the creator
    groups_query = Group.query.all()
    print('groups',groups_query)
    groups = []
    for group in groups_query:
        groups.append({
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "created_at": group.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    print('Groups created by user:', user_id, groups)
    return jsonify(groups=groups)
# Join an existing group
@groups_bp.route('/<int:group_id>/join', methods=['POST'])
@jwt_required()
def join_group(group_id):
    user_id = get_jwt_identity()  # Get user from JWT token
    group = Group.query.get_or_404(group_id)

    # Check if the user is already a member of the group
    existing_membership = Membership.query.filter_by(user_id=user_id, group_id=group_id).first()
    if existing_membership:
        return jsonify({"msg": "You are already a member of this group"}), 400

    # Add the user as a member of the group
    membership = Membership(user_id=user_id, group_id=group_id, role='member')
    db.session.add(membership)
    db.session.commit()

    return jsonify({"msg": f"Joined group {group.name} successfully"}), 200

# Leave a group
@groups_bp.route('/<int:group_id>/leave', methods=['POST'])
@jwt_required()
def leave_group(group_id):
    user_id = get_jwt_identity()  # Get user from JWT token
    membership = Membership.query.filter_by(user_id=user_id, group_id=group_id).first()

    if not membership:
        return jsonify({"msg": "You are not a member of this group"}), 400

    # Remove the user from the group
    db.session.delete(membership)
    db.session.commit()

    return jsonify({"msg": "You left the group successfully"}), 200
