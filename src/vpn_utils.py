import tkinter as tk
from popup_window import popup_window

def connect_vpn():
    instructions = (
        "To connect to the VPN, please follow these steps:\n\n"
        "1. Click on the Wi-Fi icon at the top right corner of the screen.\n"
        "2. Navigate to the VPN section within the network settings.\n"
        "3. Enable the VPN connection by clicking on the vpn button top right."
    )
    popup_window("Connect to VPN", instructions)
