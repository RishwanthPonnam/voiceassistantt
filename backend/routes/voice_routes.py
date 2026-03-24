from flask import Blueprint, request, jsonify
from utils.helper import process_voice_command, text_to_speech

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

@voice_bp.route('/synthesize', methods=['POST'])
def synthesize_speech():
    """Convert text to speech"""
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate audio
        audio_data = text_to_speech(text)
        
        return jsonify({
            'text': text,
            'audio': audio_data,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
