"""
Voice Assistant Web Application Entry Point
"""

import os
import sys

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from backend.app import app

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Voice Assistant Web Application")
    print("=" * 50)
    print("\nServer running at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
