import os
import platform
import subprocess

def open_pdf(filepath):
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", filepath])
    else:  # Linux
        subprocess.call(["xdg-open", filepath])
