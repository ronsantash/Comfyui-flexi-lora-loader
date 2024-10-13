import os
import re

# Full path to the lora.py file
lora_file_path = 'E:/ComfyUI_windows_portable/ComfyUI/comfy/lora.py'

# Verify if the lora.py file exists
if os.path.exists(lora_file_path):
    with open(lora_file_path, 'r') as file:
        lora_contents = file.read()
    # Extract all function names using regex
    functions = re.findall(r'def\s+(\w+)\s*\(', lora_contents)
    print("Functions in lora.py:", functions)
else:
    print('lora.py not found')

