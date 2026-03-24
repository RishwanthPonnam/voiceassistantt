from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from utils.helper import process_voice_command, send_whatsapp_message, open_whatsapp_web

voice_bp = Blueprint('voice', __name__, url_prefix='/api/voice')

@voice_bp.route('/process', methods=['POST'])
def process_voice():
    """Process voice command from user"""
    try:
        data = request.json
        command = data.get('command')
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        # Process the voice command
        response = process_voice_command(command)
        
        return jsonify({
            'command': command,
            'response': response,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@voice_bp.route('/whatsapp/open', methods=['POST'])
def whatsapp_open():
    """Open WhatsApp and prompt for task"""
    try:
        success, message = open_whatsapp_web()
        return jsonify({
            'success': success,
            'message': message,
            'status': 'opened',
            'prompt': '📱 WhatsApp is opened! What task would you like me to do? Say: "message [contact] [message]"'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@voice_bp.route('/whatsapp/send', methods=['POST'])
def whatsapp_send():
    """Send WhatsApp message"""
    try:
        data = request.json
        contact = data.get('contact')
        message = data.get('message')
        
        if not contact or not message:
            return jsonify({'error': 'Contact and message required'}), 400
        
        success, result = send_whatsapp_message(contact, message)
        
        return jsonify({
            'success': success,
            'message': result,
            'contact': contact,
            'status': 'sent' if success else 'failed'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
