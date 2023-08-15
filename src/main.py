import tkinter as tk
from tkinter import ttk
from pull_files_window import pull_files_window
from start_webapp import start_webapp_server
from vpn_utils import connect_vpn

# Create the main application window
app = tk.Tk()
app.title("Desktop App")
app.geometry("600x350")  # Increased size of the main window

# Create the buttons
connect_vpn_btn = tk.Button(app, text="Connect to VPN", command=connect_vpn)
pull_files_btn = tk.Button(app, text="Pull Files", command=lambda: pull_files_window(app))
start_webapp_btn = tk.Button(app, text="Start Webapp Server", command=start_webapp_server)

# Place the buttons on the window
connect_vpn_btn.pack(pady=10)
pull_files_btn.pack(pady=10)
start_webapp_btn.pack(pady=10)

# Start the main event loop
app.mainloop()
