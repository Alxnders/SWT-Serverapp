import tkinter as tk
from popup_window import popup_window
import subprocess

def start_webapp_server():
    directory_path = "/home/user/Desktop/webapp"
    command = ["gnome-terminal", "--", "npm", "start"]

    try:
        # Change the current working directory to the specified directory
        subprocess.run(command, cwd=directory_path, check=True)
    except subprocess.CalledProcessError:
        print("Error executing the command.")
