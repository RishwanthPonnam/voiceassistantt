"""Helper functions for the Voice Assistant"""

import subprocess
import os
import re
import glob
from datetime import datetime
import winreg

# Application paths for Windows (primary locations)
APPLICATIONS = {
    'whatsapp': [
        'C:\\Program Files\\WindowsApps\\5A0681DE511B2_*\\WhatsApp.exe',
        'C:\\Users\\*\\AppData\\Local\\WhatsApp\\app-*\\WhatsApp.exe',
        'C:\\Users\\*\\AppData\\Local\\Microsoft\\WindowsApps\\WhatsApp.exe',
    ],
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
        paths = [paths]
    
    # Try each path with environment variable expansion and wildcard support
    for path in paths:
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
    
    # Try Windows Registry as fallback
    registry_path = find_app_in_registry(app_name)
    if registry_path:
        return registry_path
    
    return None

def find_app_in_registry(app_name):
    """
    Try to find application path in Windows Registry
    
    Args:
        app_name (str): Name of the application
    
    Returns:
        str: Path to application or None
    """
    try:
        # Common registry paths for applications
        registry_paths = [
            r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths',
            r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\App Paths',
        ]
        
        for registry_path in registry_paths:
            try:
                reg_key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    registry_path
                )
                try:
                    subkey, _ = winreg.QueryValueEx(reg_key, app_name)
                    if os.path.exists(subkey):
                        return subkey
                except WindowsError:
                    pass
                finally:
                    winreg.CloseKey(reg_key)
            except WindowsError:
                pass
    except Exception as e:
        pass
    
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
        available_apps = ', '.join(sorted(APPLICATIONS.keys()))
        return False, f'❌ Application "{app_name}" not found. Available: {available_apps}'
    
    try:
        if app_path.startswith('ms-'):
            # Handle Windows URI schemes
            os.startfile(app_path)
        else:
            subprocess.Popen(app_path)
        return True, f'✅ Opening {app_name}...'
    except Exception as e:
        return False, f'❌ Error opening {app_name}: {str(e)}'

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
        return f'📝 You said: "{command}". How can I help you? Try "open chrome" or "what time is it?"'

