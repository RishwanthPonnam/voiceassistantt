"""Helper functions for the Voice Assistant"""

import subprocess
import os
import re
from datetime import datetime

# Application paths for Windows
APPLICATIONS = {
    'whatsapp': ['C:\\Program Files\\WindowsApps\\5A0681DE511B2_*\\WhatsApp.exe', 'C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\app-*\\WhatsApp.exe'],
    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'firefox': 'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
    'edge': 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'notepad': 'C:\\Windows\\System32\\notepad.exe',
    'calculator': 'C:\\Windows\\System32\\calc.exe',
    'paint': 'C:\\Windows\\System32\\mspaint.exe',
    'explorer': 'C:\\Windows\\explorer.exe',
    'settings': 'ms-settings:',
    'word': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
    'excel': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
    'powerpoint': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
}

def find_application_path(app_name):
    """
    Find the actual path of an application
    
    Args:
        app_name (str): Name of the application
    
    Returns:
        str: Path to the application or None
    """
    if app_name not in APPLICATIONS:
        return None
    
    paths = APPLICATIONS[app_name]
    if isinstance(paths, str):
        paths = [paths]
    
    for path in paths:
        # Expand environment variables
        path = os.path.expandvars(path)
        
        # Handle wildcards using glob
        if '*' in path:
            import glob
            matches = glob.glob(path)
            if matches:
                return matches[0]
        elif os.path.exists(path):
            return path
    
    return None

def open_application(app_name):
    """
    Open an application by name
    
    Args:
        app_name (str): Name of the application to open
    
    Returns:
        tuple: (success: bool, message: str)
    """
    app_name = app_name.lower().strip()
    app_path = find_application_path(app_name)
    
    if not app_path:
        return False, f'Application "{app_name}" not found on this system. Available apps: {", ".join(APPLICATIONS.keys())}'
    
    try:
        subprocess.Popen(app_path)
        return True, f'Opening {app_name}...'
    except Exception as e:
        return False, f'Error opening {app_name}: {str(e)}'

def process_voice_command(command):
    """
    Process voice commands and return appropriate response
    
    Args:
        command (str): Voice command from user
    
    Returns:
        str: Response to the command
    """
    command_lower = command.lower().strip()
    
    # Check for "open application" command
    if command_lower.startswith('open ') or 'open' in command_lower:
        # Extract application name
        match = re.search(r'open\s+(\w+)', command_lower)
        if match:
            app_name = match.group(1)
            success, message = open_application(app_name)
            return message
    
    # Simple command processing logic
    if 'hello' in command_lower or 'hi' in command_lower:
        return 'Hello! How can I assist you today?'
    
    elif 'weather' in command_lower:
        return 'I am unable to fetch weather data at the moment.'
    
    elif 'time' in command_lower:
        current_time = datetime.now().strftime('%H:%M:%S')
        return f'The current time is {current_time}'
    
    elif 'date' in command_lower:
        current_date = datetime.now().strftime('%A, %B %d, %Y')
        return f'Today is {current_date}'
    
    elif 'help' in command_lower:
        return 'You can ask me to: open applications (whatsapp, chrome, firefox, etc.), tell time, date, weather, or just chat with me!'
    
    else:
        return f'You said: {command}. How can I help? Try saying "open whatsapp" or "what time is it"'

