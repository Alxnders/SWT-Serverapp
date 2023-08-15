import tkinter as tk

def popup_window(title, message):
    popup = tk.Toplevel()
    popup.title(title)
    popup.geometry("400x150")  # Increased size to accommodate more text
    popup_label = tk.Label(popup, text=message, padx=10, pady=10)
    popup_label.pack()