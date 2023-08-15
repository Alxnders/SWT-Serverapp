import tkinter as tk
from tkinter import ttk
from popup_window import popup_window
from pull_files_utils import add_machine_sub, add_machine_com, remove_machine, pull_files_go
from vars import vars

def pull_files_window(app):
    
    pull_files_popup = tk.Toplevel(app)
    pull_files_popup.title("Pull Files")
    pull_files_popup.geometry("500x350")

    machines_var = tk.StringVar()
    machine_var_sub = tk.StringVar()

    machine_list = ["10.2.2.44", "10.2.2.42", "10.2.2.41", "10.2.2.40", "10.2.2.34", "10.2.2.30", "10.2.2.26", "10.2.2.24", "10.2.2.17"]
    machines_var.set(machine_list[0])

    machines_combobox = ttk.Combobox(pull_files_popup, values=machine_list, textvariable=machines_var)
    machines_combobox.grid(row=0, column=0, padx=10, pady=10)

    add_combo_btn = tk.Button(pull_files_popup, text="Add", command=lambda: add_machine_com(machines_combobox, machines_display))
    add_combo_btn.grid(row=0, column=1, padx=5, pady=10)

    machines_display = tk.Listbox(pull_files_popup)
    machines_display.grid(row=0, column=2, padx=10, pady=10)
    for machine in vars.machines_list:
        machines_display.insert(tk.END, machine)

    remove_btn = tk.Button(pull_files_popup, text="Remove", command=lambda: remove_machine(machines_display))
    remove_btn.grid(row=1, column=2, padx=5, pady=5)

    machine_entry_sub = tk.Entry(pull_files_popup, textvariable=machine_var_sub)
    machine_entry_sub.grid(row=1, column=0, padx=10, pady=0)
    machine_entry_sub.bind("<Return>", lambda event: add_machine_sub(machine_var_sub, machines_display))

    add_btn_sub = tk.Button(pull_files_popup, text="Add", command=lambda: add_machine_sub(machine_var_sub, machines_display))
    add_btn_sub.grid(row=1, column=1, padx=5, pady=10)

    go_btn_pull_files = tk.Button(pull_files_popup, text="Go", command=lambda: pull_files_go(vars.machines_list, vars.vpn))
    go_btn_pull_files.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    pull_files_popup.mainloop()
