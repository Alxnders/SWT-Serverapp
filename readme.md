# ServerApp

This project allows you to seamlessly interact with SWT machines through SSH and SCP for the [**SWT webapp**](https://github.com/Alxnders/SWT-webapp). Below, you'll find instructions on how to set up and use the project effectively.

## Prerequisites

Before you get started, make sure you have the following:

- [Python](https://www.python.org/downloads/) installed on your system.
- Access to the machines you want to interact with via SSH and SCP.
- The `ssh.key` file containing the SSH password for the machines.
- [Optional] The SWT-Webapp project to be able to interact with the data.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone git@github.com:Alxnders/SWT-Serverapp.git
   cd project-name

2. Place your **ssh.key** file in either the **/src/keys** directory or the **/dist/keys** directory, depending on which one you want to use.
(Note : You'll probably have to modify certain paths in pull_files_utils.py to get this to fully work.)

## Usage
1. Navigate to the /src directory:

    ```bash
    cd src

2. Run the main Python script:

    ```bash
    python main.py

This will launch the application and provide you with various options to interact with the machines.

Alternatively, you can also use the executable located in the /dist/serverapp directory. Simply double-click the serverapp executable to start the application.
But you wont be able to use the scp functionnalities of the app.

## Features
- [Connect To VPN]: Explaination for non-IT people on how to connect to the vpn on a specific ubuntu computer.
- [Pull Files]: Opens a new page where you can select, or manually input, a machine (using its IP on a private VPN Network) add it to a list and then fetch all the data files that are needed to display its data on the Webapp project.
- [Start Webapp Server] : Starts the webapp server. Look into start_webapp.py to modify the path if needed.

## Contact
Alexander SAUVIGNET alexander.sauvignet@stockholmwater.com.
