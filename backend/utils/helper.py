"""Helper functions for the Voice Assistant"""

import subprocess
import os
import re
import glob
from datetime import datetime
import webbrowser
import time
import threading

# Try importing optional dependencies for WhatsApp automation
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

try:
    from pynput.keyboard import Controller, Key
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

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
        return True, '✅ WhatsApp Web opened! Please log in if needed...'
    except Exception as e:
        return False, f'❌ Error opening WhatsApp Web: {str(e)}'

def send_whatsapp_message(contact_name, message_text):
    """
    Send a message through WhatsApp Web
    
    Args:
        contact_name (str): Name of the contact to message
        message_text (str): Text message to send
    
    Returns:
        tuple: (success: bool, message: str)
    """
    if not PYPERCLIP_AVAILABLE or not PYNPUT_AVAILABLE:
        return False, '❌ WhatsApp automation not available. Please install required packages: pyperclip and pynput'
    
    try:
        keyboard = Controller()
        
        # Ensure WhatsApp Web is open
        webbrowser.open('https://web.whatsapp.com')
        time.sleep(2)
        
        # Click on search box (using keyboard shortcut)
        keyboard.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # Type contact name
        pyperclip.copy(contact_name)
        keyboard.hotkey('ctrl', 'v')
        time.sleep(1)
        
        # Press Enter to select first result
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(1)
        
        # Click on message input field
        keyboard.hotkey('tab')
        time.sleep(0.5)
        
        # Type and send message
        pyperclip.copy(message_text)
        keyboard.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # Send message (Ctrl+Enter or just Enter)
        keyboard.hotkey('ctrl', Key.enter)
        time.sleep(1)
        
        return True, f'✅ Message sent to {contact_name}: "{message_text}"'
    except Exception as e:
        return False, f'❌ Error sending WhatsApp message: {str(e)}'

def parse_whatsapp_command(command):
    """
    Parse WhatsApp-specific commands to extract contact and message
    
    Args:
        command (str): Voice command text
    
    Returns:
        tuple: (contact_name, message_text) or (None, None) if not a valid command
    """
    # Pattern: "message [contact] [message]" or "send message to [contact] [message]"
    
    # Try pattern: "message to [contact] [message]"
    match = re.search(r'message\s+to\s+(.+?)\s+(.+)', command, re.IGNORECASE)
    if match:
        contact = match.group(1).strip()
        message = match.group(2).strip()
        return contact, message
    
    # Try pattern: "send [message] to [contact]"
    match = re.search(r'send\s+(.+?)\s+to\s+(.+)', command, re.IGNORECASE)
    if match:
        message = match.group(1).strip()
        contact = match.group(2).strip()
        return contact, message
    
    # Try pattern: "[contact] [message]" (after "open whatsapp")
    match = re.search(r'([A-Za-z\s]+)\s+(.+)', command)
    if match and len(match.group(1).split()) <= 3:  # Assume contact name is max 3 words
        contact = match.group(1).strip()
        message = match.group(2).strip()
        return contact, message
    
    return None, None

def process_voice_command(command):
    """
    Process voice commands and return appropriate response
    
    Args:
        command (str): Voice command from user
    
    Returns:
        str: Response to the command
    """
    command_lower = command.lower().strip()
    
    # Check for WhatsApp messaging commands
    if 'whatsapp' in command_lower and ('message' in command_lower or 'send' in command_lower or 'text' in command_lower):
        # Extract contact and message
        task = command_lower.replace('open whatsapp', '').replace('and', '').strip()
        contact, message = parse_whatsapp_command(task)
        
        if contact and message:
            # Open WhatsApp and send message
            success, result = open_whatsapp_web()
            if success:
                # Give user time to see WhatsApp opened
                time.sleep(2)
                
                # Now try to send the message
                send_success, send_msg = send_whatsapp_message(contact, message)
                if send_success:
                    return f'✅ WhatsApp opened and message sent to {contact}: "{message}"'
                else:
                    return f'⚠️ WhatsApp opened but could not send automatically. Please send message manually to {contact}: "{message}"'
            return result
        else:
            return '📱 WhatsApp message command detected. Please say: "message [contact name] [your message]"'
    
    # Check for simple "open application" command
    if command_lower.startswith('open ') or 'open' in command_lower:
        # Extract application name
        match = re.search(r'open\s+([\w\s-]+)', command_lower)
        if match:
            app_name = match.group(1).strip()
            # Remove extra words
            app_name = re.sub(r'\s+(and|to|message|text).*', '', app_name).strip()
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
        return '📖 You can: open applications (whatsapp, chrome, teams, etc), send WhatsApp messages (say "message [contact] [message]"), check time/date, or just chat!'
    
    elif 'thank' in command_lower:
        return '😊 You\'re welcome! Happy to help!'
    
    else:
        return f'📝 You said: "{command}". Try: "open whatsapp message John hello" or "what time is it?"'

