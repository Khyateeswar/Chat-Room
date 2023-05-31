import socket
import threading
YELLOW = "\033[1;33m " 
BLUE = "\033[1;34m "
GREEN =  "\033[1;32m "
RED =  "\033[1;31m "
PINK = "\033[1;35m "
CYAN = "\033[1;36m "
GREY = "\033[1;30m "
WHITE = "\033[1;37m "




ip = input(BLUE+"Enter Ip_Address of the Server: ")
port = input(BLUE+"Enter the port number of the Server: ")
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip,int(port)))
ports = (s.recv(1024).decode()).split()
s.close()
sock_send = s
register_send = True
ready = True
sent = False
name=""
open = True
def client_send():
    global sock_send
    global register_send
    global name
    global ports
    global sent
    global open
    global ip
    global YELLOW
    global GREEN
    global RED
    global BLUE
    global WHITE
    global CYAN
    global PINK
    global GREY
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,int(ports[0])))
    sock_send= s
    while register_send:
        name = input(BLUE+"Enter Username: ")
        s.send(("REGISTER TOSEND "+name).encode())
        mll = s.recv(1024).decode()
        m = (mll).split()
        if(m[0]=="REGISTERED"):
            if(m[1]=="TOSEND"):
                register_send = False
        else:
            print(RED+"<server>"+mll)
    while open:
        msg = input(GREEN+"<You>")
        ml = msg.split()
        if(ml[0][0:1]=="@"):
            cl = ml[0][1:]
            if(cl!="ALL"):
                sent = True
            n=len(ml[0])+1
            body = msg[n:]
            length = len(body)
            s.send(("SEND "+cl+" "+str(n)+" "+body).encode())
        elif (ml[0]=="close"):
            s.send("close".encode())
            open = False
        else:
            print(RED+"Message not in format type again")
        while sent:
            if(sent == False):
                break
    s.close()

        


def client_recieve():
    global sock_send
    global register_send
    global name
    global ports
    global sent
    global open
    global ip
    global ready
    global YELLOW
    global GREEN
    global RED
    global BLUE
    global WHITE
    global CYAN
    global PINK
    global GREY
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,int(ports[1])))
    while ready:
        if not register_send:
            ready = False
    s.send(("REGISTER TORECV "+name).encode())
    m = (s.recv(1024).decode()).split()
    print("Welcome to the chat room!!!")
    while open:
        msgl=s.recv(1024).decode()
        msg = (msgl).split()
        n=len(msg)
        if(n==0):
            break
        if (msg[0]=="FORWARD"):
            sender = msg[1]
            body = ""
            for i in range(3,n):
                body = body+msg[i]+" "
            print(CYAN+"                                    <"+sender+">"+body+GREEN)
            sock_send.send(("RECIEVED "+sender).encode())
        elif(msg[0]=="BROADCAST"):
            sender = msg[1]
            body = ""
            for i in range(3,n):
                body = body+msg[i]+" "
            str = "<"+sender+">"+body
            print(PINK+"                                    " +str+GREEN)
        elif (msg[0]=="ERROR"):
            print(RED+"<server>"+msgl+GREEN)
            sent = False
        else:
            sent = False
    s.close()

send=threading.Thread(target=client_send)
recv = threading.Thread(target=client_recieve)
send.start()
recv.start()
while open:
    if(open == False):
        break






                
    









