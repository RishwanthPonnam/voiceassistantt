#!/usr/bin/env python
"""
Git sync script using subprocess for reliable execution
"""
import subprocess
import sys
import os

os.chdir(r'C:\Users\Rishwanth\Desktop\voiceassistant')

print("=" * 50)
print(" Git Sync Process")
print("=" * 50)
print()

commands = [
    ("Pull from GitHub", ["git", "pull", "origin", "main"]),
    ("Stage changes", ["git", "add", "backend/utils/helper.py", "backend/utils/app_finder.py", "sync.ps1", "sync.bat"]),
    ("Commit changes", ["git", "commit", "-m", "feat: Add WhatsApp Web fallback and advanced app finder"]),
    ("Push to GitHub", ["git", "push", "origin", "main"]),
    ("Show final status", ["git", "status"]),
]

for step_name, cmd in commands:
    print(f"\n[*] {step_name}...")
    print(f"    Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.stdout:
            print(f"    Output: {result.stdout[:200]}")
        if result.stderr and "fatal" in result.stderr.lower():
            print(f"    Error: {result.stderr[:200]}")
            print(f"    FAILED - Exit code: {result.returncode}")
        else:
            print(f"    ✓ Success")
    except Exception as e:
        print(f"    ✗ Exception: {str(e)}")

print()
print("=" * 50)
print(" Sync Complete!")
print("=" * 50)
