from flask import Blueprint, request, jsonify
from models.message_model import db, Message
from datetime import datetime

message_bp = Blueprint('messages', __name__, url_prefix='/api/messages')

@message_bp.route('/', methods=['GET'])
def get_messages():
    """Get all messages"""
    try:
        messages = Message.query.all()
        return jsonify([{
            'id': msg.id,
            'user_message': msg.user_message,
            'assistant_response': msg.assistant_response,
            'timestamp': msg.timestamp
        } for msg in messages]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@message_bp.route('/', methods=['POST'])
def create_message():
    """Create a new message"""
    try:
        data = request.json
        message = Message(
            user_message=data.get('user_message'),
            assistant_response=data.get('assistant_response')
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({
            'id': message.id,
            'user_message': message.user_message,
            'assistant_response': message.assistant_response,
            'timestamp': message.timestamp
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@message_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """Delete a message"""
    try:
        message = Message.query.get(message_id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
