"""
Advanced Application Finder for Windows
Searches for applications in all possible locations
"""

import os
import glob
import subprocess
from pathlib import Path
import winreg

def scan_windows_start_menu():
    """Scan Windows Start Menu for application shortcuts"""
    apps = {}
    start_menu_paths = [
        os.path.expandvars(r'%ProgramData%\Microsoft\Windows\Start Menu\Programs'),
        os.path.expandvars(r'%AppData%\Microsoft\Windows\Start Menu\Programs'),
    ]
    
    for menu_path in start_menu_paths:
        if not os.path.exists(menu_path):
            continue
            
        for lnk in glob.glob(os.path.join(menu_path, '**', '*.lnk'), recursive=True):
            try:
                app_name = Path(lnk).stem.lower()
                apps[app_name] = lnk
            except:
                pass
    
    return apps

def get_installed_apps_from_registry():
    """Get list of all installed applications from Windows Registry"""
    apps = {}
    registry_paths = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
    
    for reg_path in registry_paths:
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            num_subkeys = winreg.QueryInfoKey(registry_key)[0]
            
            for i in range(num_subkeys):
                subkey_name = winreg.EnumKey(registry_key, i)
                subkey = winreg.OpenKey(registry_key, subkey_name)
                
                try:
                    display_name, _ = winreg.QueryValueEx(subkey, 'DisplayName')
                    install_location, _ = winreg.QueryValueEx(subkey, 'InstallLocation')
                    
                    app_key = display_name.lower().replace(' ', '')
                    apps[app_key] = {
                        'name': display_name,
                        'path': install_location
                    }
                except:
                    pass
                finally:
                    winreg.CloseKey(subkey)
            
            winreg.CloseKey(registry_key)
        except:
            pass
    
    return apps

def find_whatsapp():
    """
    Specifically search for WhatsApp in all possible locations
    
    Returns:
        str: Path to WhatsApp executable or None
    """
    # Common WhatsApp installation locations
    whatsapp_paths = [
        #Windows Store version
        os.path.expandvars(r'%ProgramFiles%\WindowsApps\5A0681DE511B2_*\WhatsApp.exe'),
        os.path.expandvars(r'%ProgramFiles(x86)%\WindowsApps\5A0681DE511B2_*\WhatsApp.exe'),
        
        # Portable/Manual installation
        os.path.expandvars(r'%LocalAppData%\WhatsApp\app-*\WhatsApp.exe'),
        os.path.expandvars(r'%LocalAppData%\WhatsApp\bin\WhatsApp.exe'),
        os.path.expandvars(r'%LocalAppData%\Microsoft\WindowsApps\WhatsApp.exe'),
        
        # Program Files
        os.path.expandvars(r'%ProgramFiles%\WhatsApp\WhatsApp.exe'),
        os.path.expandvars(r'%ProgramFiles(x86)%\WhatsApp\WhatsApp.exe'),
        
        # Desktop
        os.path.expandvars(r'%UserProfile%\Desktop\WhatsApp.exe'),
        os.path.expandvars(r'%UserProfile%\Desktop\WhatsApp\WhatsApp.exe'),
    ]
    
    for pattern in whatsapp_paths:
        if '*' in pattern:
            matches = glob.glob(pattern)
            if matches:
                # Sort by modification time (newest first)
                matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                for match in matches:
                    if os.path.exists(match):
                        print(f"✓ WhatsApp found at: {match}")
                        return match
        else:
            if os.path.exists(pattern):
                print(f"✓ WhatsApp found at: {pattern}")
                return pattern
    
    print("❌ WhatsApp not found in standard locations")
    return None

def find_application_by_name(app_name):
    """
    Find application executable by name (comprehensive search)
    
    Args:
        app_name (str): Name of application (e.g., 'whatsapp', 'chrome')
    
    Returns:
        str: Path to application or None
    """
    app_name_lower = app_name.lower().strip()
    
    # Special handling for WhatsApp
    if 'whatsapp' in app_name_lower:
        return find_whatsapp()
    
    # Try registry first
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths'
        )
        try:
            apppath, _ = winreg.QueryValueEx(registry_key, app_name)
            if os.path.exists(apppath):
                return apppath
        except WindowsError:
            pass
        finally:
            winreg.CloseKey(registry_key)
    except:
        pass
    
    # Try common program file locations
    common_paths = [
        os.path.expandvars(f'%ProgramFiles%\\{app_name}\\{app_name}.exe'),
        os.path.expandvars(f'%ProgramFiles(x86)%\\{app_name}\\{app_name}.exe'),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

if __name__ == '__main__':
    # Test the functions
    print("Searching for WhatsApp...")
    whatsapp_path = find_whatsapp()
    if whatsapp_path:
        print(f"Found: {whatsapp_path}")
    else:
        print("WhatsApp not found. Checking installed apps from registry...")
        apps = get_installed_apps_from_registry()
        whatsapp_apps = {k: v for k, v in apps.items() if 'whatsapp' in k.lower()}
        if whatsapp_apps:
            print("WhatsApp-related apps found:")
            for k, v in whatsapp_apps.items():
                print(f"  {v.get('name', k)}: {v.get('path', 'Unknown')}")
