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


clients_s=[]
clients_r=[]
connections={}
sockets={}
rec_port={}
ports=[]
for i in range (200):
    ports.append(i+1200)
port = int(input(BLUE+"Enter port number for the server: "))
def server_recieve(ip,port_number):
    global clients_s
    global clients_r
    global connections
    global sockets
    global rec_port
    global ports
    global YELLOW
    global GREEN
    global RED
    global BLUE
    global WHITE
    global CYAN
    global PINK
    global GREY
    def send_msg(conn,sms):
        conn.send((sms).encode())
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostbyname(socket.gethostname()),port_number))
    s.listen(5)
    open = True
    name=""
    while open:
        conn,addr  = s.accept()
        if(addr[0]!=ip):
            conn.close
        else:
            register = True
            while register:
                stat = conn.recv(1024).decode()
                req1 = (stat).split()
                #print(stat)
                if(req1[0]=="REGISTER"):
                    if(req1[1]=="TOSEND"):
                        name = req1[2]
                        print(name)
                        if (name in clients_s) or (name == "ALL") or ( not (name.isalnum())):
                            send_msg(conn,"ERROR 100 Malformed username")
                        else:
                            clients_s.append(name)
                            send_msg(conn,"REGISTERED TOSEND "+name)
                            register = False
                    else:
                        send_msg(conn,"ERROR 101 No user registered")
                else:
                    send_msg(conn,"ERROR 101 No user registered")
            conn_open = True
            jo = name+" joined"
            print(YELLOW+jo)
            for c in connections.values():
                send_msg(c,"BROADCAST "+"server "+str(len(jo))+" "+jo)
            while conn_open:
                req = (conn.recv(1024).decode()).split()
                if(req[0]=="SEND"):
                    if(req[2].isnumeric()) and (int(req[2])<1024):
                        msg=""
                        for i in range(3,len(req)):
                            msg = msg+req[i]+" "
                        if req[1] in clients_r:
                            send_msg(connections[req[1]],"FORWARD "+name+" "+req[2]+" "+msg)
                        elif (req[1] == "ALL"):
                            for c in connections.values():
                                if(c!=connections[name]):
                                    send_msg(c,"BROADCAST "+name+" "+req[2]+" "+msg)
                        else:
                             send_msg(connections[name],"ERROR 102 Unable to send")
                    else:
                        send_msg(connections[name],"ERROR 103 Header incomplete")
                elif(req[0]=="close"):
                    conn_open = False
                elif(req[0]=="RECIEVED"):
                    ack = req[1]
                    send_msg(connections[ack],"SENT "+name)
                else:
                    send_msg(connections[name],"ERROR 103 Header incomplete")
            lo = name+" left"
            for c in connections.values():
                if(c!=connections[name]):
                    send_msg(c,"BROADCAST "+"server "+str(len(lo))+" "+lo)
            conn.close()
            connections[name].close()
            sockets[name].close()
            ports.append(rec_port[name])
            del rec_port[name]
            del sockets[name]
            del connections[name]
            clients_r.remove(name)
            clients_s.remove(name)
            open = False
    s.close()
    ports.append(port_number)
    print(RED+name +" left")

def server_send(ip,port_number):
    global clients_s
    global clients_r
    global connections
    global sockets
    global rec_port
    global ports
    def send_msg(conn,sms):
        conn.send((sms).encode())
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((socket.gethostbyname(socket.gethostname()),port_number))
    s.listen(5)
    name=""
    open = True
    while open:
        conn,addr=s.accept()
        if(addr[0]!=ip):
            conn.close
        else:
            register = True
            while register:
                req1 = (conn.recv(1024).decode()).split()
                if(req1[0]=="REGISTER"):
                    if(req1[1]=="TORECV"):
                        name = req1[2]
                        if name in clients_r:
                            send_msg(conn,"ERROR 100 Malformed username")
                        else:
                            clients_r.append(name)
                            send_msg(conn,"REGISTERED TORECV "+name)
                            register = False
                            connections[name]=conn
                            sockets[name]=s
                            rec_port[name]=port_number
                    else:
                        send_msg(conn,"ERROR 101 No user registered")
                else:
                    send_msg(conn,"ERROR 101 No user registered")
            if register==False:
                break

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostbyname(socket.gethostname()),port))
s.listen(5)
print(YELLOW+"SERVER IS WORKING ")
while True:
    if(len(clients_s)<100):
        conn,addr = s.accept()
        print(GREEN+addr[0]+" is connected")
        conn.send((str(ports[0])+" "+str(ports[1])).encode())
        send = threading.Thread(target=server_recieve,args = (addr[0],ports[0],))
        recieve = threading.Thread(target=server_send,args=(addr[0],ports[1]))
        send.start()
        recieve.start()
        ports.pop(0)
        ports.pop(0)
        conn.close()
    else:
        continue
    


