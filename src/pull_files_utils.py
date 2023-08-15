import tkinter as tk
from tkinter import ttk
from popup_window import popup_window
from vars import vars
import subprocess
import os
import sys
import re
import datetime

def is_valid_ip(ip):
    # Regular expression to match a valid IP address format x.x.x.x
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return re.match(ip_pattern, ip)

def add_machine_sub(machine_var_sub, machines_display):
    selected_machine_sub = machine_var_sub.get()

    if is_valid_ip(selected_machine_sub) and selected_machine_sub not in vars.machines_list:
        vars.machines_list.append(selected_machine_sub)
        machines_display.insert(tk.END, selected_machine_sub)
        machine_var_sub.set("")  # Clear the input zone
    elif selected_machine_sub:
        popup_window("Error", "Invalid or duplicate IP address.")
    else:
        popup_window("Error", "Please enter a valid IP address.")

def add_machine_com(machines_combobox, machines_display):
    selected_machine = machines_combobox.get()
    
    if selected_machine and selected_machine not in vars.machines_list:
        vars.machines_list.append(selected_machine)
        machines_display.insert(tk.END, selected_machine)
    elif selected_machine:
        popup_window("Error", "Machine already in the list.")
    else:
        popup_window("Error", "Please select a machine from the combo box.")

def remove_machine(machines_display):
    selected_index = machines_display.curselection()
    if selected_index:
        machine = machines_display.get(selected_index)
        vars.machines_list.remove(machine)
        machines_display.delete(selected_index)

def get_ssh_password():
    if getattr(sys, 'frozen', False):
        # The application is frozen (i.e., running as a standalone executable)
        script_dir = os.path.dirname(sys.executable)
    else:
        # The application is running in a normal Python environment
        script_dir = os.path.dirname(os.path.abspath(__file__))

    keys_dir = os.path.join(script_dir, "keys")
    key_file_path = os.path.join(keys_dir, "ssh.key")

    if not os.path.exists(key_file_path):
        raise FileNotFoundError("ssh.key file not found in the 'keys' directory.")

    with open(key_file_path, 'r') as password_file:
        password = password_file.read().strip()

    return password

def get_logs_directory():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    logs_dir = os.path.join(base_dir, "logs")

    # Ensure the logs directory exists
    os.makedirs(logs_dir, exist_ok=True)

    return logs_dir


def pull_files_go(machines_list, vpn):
    ssh_password = get_ssh_password()
    vpn = True
    if machines_list:
        if vpn:
            source_user = "pi"
            source_directory = "~/phoenix/data/"
            destination_directory = "/home/user/Desktop/webapp/server/raw/"
            prep_directory = "/home/user/Desktop/webapp/server/data/"

            total_machines = len(machines_list)

            log_filename = os.path.join(get_logs_directory(), datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log")

            # Create the progress popup
            progress_popup = tk.Toplevel()
            progress_popup.title("Copying Files")
            progress_popup.geometry("300x100")

            title_label = tk.Label(progress_popup, text="Copying files...", padx=10, pady=10)
            title_label.pack()

            progress_bar = ttk.Progressbar(progress_popup, orient="horizontal", length=200, mode="determinate")
            progress_bar.pack()

            progress_popup.update()

            with open(log_filename, "a") as log_file:
                for index, machine in enumerate(machines_list):
                    try:
                        log_file.write(f"[{datetime.datetime.now()}] Pulling files from {machine}...\n")
                        title_label.config(text=f"Copying files from {machine} ...")

                        source_address = f"{source_user}@{machine}:{source_directory}*"
                        destination_address = f"{destination_directory}f{machine}"

                        os.makedirs(destination_directory, exist_ok=True)

                        command = [
                            "sshpass", "-p", ssh_password,
                            "scp", "-r",
                            source_address, destination_address
                        ]

                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate()

                        if process.returncode == 0:
                            log_file.write(f"[{datetime.datetime.now()}] Files pulled successfully from {machine}.\n")
                        else:
                            log_file.write(f"[{datetime.datetime.now()}] Error pulling files from {machine}: {stderr.decode('utf-8')}\n")
                            disconnected = True

                        log_file.write(f"[{datetime.datetime.now()}] Prepping files from {machine}...\n")

                        destination_address = f"{destination_directory}f{machine}"
                        prep_directory_dir = f"{prep_directory}f{machine}"
                        prep_directory_adress = f"{prep_directory_dir}/prep.dat"

                        os.makedirs(prep_directory_dir, exist_ok=True)

                        command = f'python prep.py {destination_address}/* {prep_directory_adress}'

                        prepprocess = subprocess.run(command, shell=True)

                        if prepprocess.returncode == 0:
                            log_file.write(f"[{datetime.datetime.now()}] Prepping was successful for {machine}:\n")
                        else :
                            if disconnected :
                                log_file.write(f"[{datetime.datetime.now()}] Error prepping files from {machine} since it is disconnected. \n")
                            else :
                                log_file.write(f"[{datetime.datetime.now()}] Error prepping files from {machine}.\n")

                    except FileNotFoundError as fe:
                        log_file.write(f"[{datetime.datetime.now()}] Error prepping files from {machine}: {fe}\n")
                    except Exception as e:
                        log_file.write(f"[{datetime.datetime.now()}] Error prepping files from {machine}: {e}\n")

            progress_bar['value'] = 100
            title_label.config(text="Files copying completed.")
            progress_popup.update()
            progress_popup.after(1000, progress_popup.destroy)  # Close the progress popup after 1 second
            print("Files copying completed.")
        else:
            popup_window("Error: VPN not connected", "Please connect to the VPN.")
    else:
        popup_window("Error", "Please add machines to the list.")