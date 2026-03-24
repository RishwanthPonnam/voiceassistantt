import subprocess
import os
import sys

os.chdir(r'C:\Users\Rishwanth\Desktop\voiceassistant')

# Add all files
subprocess.run(['git', 'add', '-A'], check=False)

# Commit with message
result = subprocess.run(
    ['git', 'commit', '-m', 'feat: Add WhatsApp Web fallback and advanced app finder utilities'],
    capture_output=True,
    text=True
)

# Push to GitHub
result = subprocess.run(
    ['git', 'push', 'origin', 'main'],
    capture_output=True,
    text=True
)

# Write results to file for verification
with open('push_result.txt', 'w') as f:
    f.write("Push operation completed\n")
    if result.returncode == 0:
        f.write("SUCCESS: Changes pushed to GitHub\n")
    else:
        f.write(f"Status: {result.returncode}\n")
    f.write(f"Output: {result.stdout}\n")
    f.write(f"Error: {result.stderr}\n")

print("Push completed - check push_result.txt for details")
