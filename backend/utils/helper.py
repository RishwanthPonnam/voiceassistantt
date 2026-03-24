"""Helper functions for the Voice Assistant"""

import subprocess
import os
import re
import glob
from datetime import datetime
import webbrowser

# Application paths for Windows (primary locations)
APPLICATIONS = {
    'whatsapp': [
        'C:\\Program Files\\WindowsApps\\5A0681DE511B2_*\\WhatsApp.exe',
        'C:\\Users\\*\\AppData\\Local\\WhatsApp\\app-*\\WhatsApp.exe',
        'C:\\Users\\*\\AppData\\Local\\Microsoft\\WindowsApps\\WhatsApp.exe',
        'whatsapp-web',  # Special flag for web version
    ],
    'whatsapp-web': 'web://whatsapp',
    'whatsapp web': 'web://whatsapp',
    'chrome': [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    ],
    'firefox': [
        'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
        'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe',
    ],
    'edge': [
        'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
        'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    ],
    'notepad': 'C:\\Windows\\System32\\notepad.exe',
    'calculator': 'C:\\Windows\\System32\\calc.exe',
    'paint': 'C:\\Windows\\System32\\mspaint.exe',
    'explorer': 'C:\\Windows\\explorer.exe',
    'settings': 'ms-settings:',
    'word': [
        'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
        'C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
    ],
    'excel': [
        'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
        'C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
    ],
    'powerpoint': [
        'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
        'C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
    ],
    'teams': [
        'C:\\Program Files\\Microsoft\\Teams\\current\\Teams.exe',
        'C:\\Users\\*\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe',
    ],
    'outlook': [
        'C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE',
        'C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE',
    ],
}

def find_application_path(app_name):
    """
    Find the actual path of an application using multiple methods
    
    Args:
        app_name (str): Name of the application
    
    Returns:
        str: Path to the application or None
    """
    if app_name not in APPLICATIONS:
        return None
    
    paths = APPLICATIONS[app_name]
    if isinstance(paths, str):
        # Handle web URLs and special schemes
        if paths.startswith('web://') or paths.startswith('ms-'):
            return paths
        paths = [paths]
    
    # Try each path with environment variable expansion and wildcard support
    for path in paths:
        # Special handling for web version
        if path == 'whatsapp-web':
            return 'web://whatsapp.com'
        
        # Expand environment variables
        expanded_path = os.path.expandvars(path)
        
        # Handle wildcards using glob
        if '*' in expanded_path:
            matches = glob.glob(expanded_path, recursive=False)
            if matches:
                # Return the first match sorted by modification time (newest first)
                matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                return matches[0]
        elif os.path.exists(expanded_path):
            return expanded_path
    
    return None

def open_application(app_name):
    """
    Open an application by name (with fallback to web version for WhatsApp)
    
    Args:
        app_name (str): Name of the application to open
    
    Returns:
        tuple: (success: bool, message: str)
    """
    app_name_original = app_name
    app_name = app_name.lower().strip()
    app_path = find_application_path(app_name)
    
    if not app_path:
        # Try to find close matches
        if 'whatsapp' in app_name:
            return open_whatsapp_web()
        
        available_apps = ', '.join(sorted(set([k.split('-')[0] for k in APPLICATIONS.keys()])))
        return False, f'❌ Application "{app_name_original}" not found. Available: {available_apps}'
    
    try:
        # Handle web URLs
        if app_path.startswith('web://'):
            webbrowser.open('https://web.whatsapp.com')
            return True, '✅ Opening WhatsApp Web in your default browser...'
        
        # Handle Windows URI schemes
        if app_path.startswith('ms-'):
            os.startfile(app_path)
            return True, f'✅ Opening {app_name_original}...'
        
        # Handle regular executables
        subprocess.Popen(app_path)
        return True, f'✅ Opening {app_name_original}...'
    except Exception as e:
        # Fallback for WhatsApp to web version
        if 'whatsapp' in app_name:
            return open_whatsapp_web()
        return False, f'❌ Error opening {app_name_original}: {str(e)}'

def open_whatsapp_web():
    """
    Open WhatsApp Web as fallback if desktop app not found
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        webbrowser.open('https://web.whatsapp.com')
        return True, '✅ WhatsApp desktop not found. Opening WhatsApp Web in your browser instead...'
    except Exception as e:
        return False, f'❌ Error opening WhatsApp Web: {str(e)}'

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
        match = re.search(r'open\s+([\w\s-]+)', command_lower)
        if match:
            app_name = match.group(1).strip()
            success, message = open_application(app_name)
            return message
    
    # Simple command processing logic
    if 'hello' in command_lower or 'hi' in command_lower:
        return '👋 Hello! How can I assist you today?'
    
    elif 'weather' in command_lower:
        return '🌤️ I am unable to fetch weather data at the moment.'
    
    elif 'time' in command_lower:
        current_time = datetime.now().strftime('%H:%M:%S')
        return f'⏰ The current time is {current_time}'
    
    elif 'date' in command_lower:
        current_date = datetime.now().strftime('%A, %B %d, %Y')
        return f'📅 Today is {current_date}'
    
    elif 'help' in command_lower:
        return '📖 You can ask me to: open applications (whatsapp, chrome, teams, outlook, excel, word, etc), tell time/date, or just chat with me!'
    
    elif 'thank' in command_lower:
        return '😊 You\'re welcome! Happy to help!'
    
    else:
        return f'📝 You said: "{command}". How can I help you? Try "open whatsapp" or "what time is it?"'

