import socket,toolbox,pickle

def Main():

    host=socket.gethostbyname(socket.gethostname()) #client ip
    port = 42451
    server = ('192.168.1.155', 42069)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    autoMode = toolbox.TFMap.get(input("1. Manual\n2. Automatic\n\nPlease choose a game mode: "))
    if autoMode:
        c = toolbox.Computer("ClientAuto",10,autoMode)
    else:
        c = toolbox.User()
    print("Game starts with you sending\nSeq:0 Ack:0 DL: 10")
    m = toolbox.message(0,0,10,0)
    while c.points != 0:
        #CREATE ANSWER pt2
        m = pickle.dumps(m)
        s.sendto(m, server)
            
        #GET MESSAGE
        data, _ = s.recvfrom(1024)
        data = pickle.loads(data)
        print(data)

        if data == None and not autoMode: 
            c.timeout(60) # TIMEOUT SURESINI 60 YAP
        m = c.receiveMessage(data)
        
    print("User lost.")
    a = toolbox.message(0, 0, 0, 1)
    a = pickle.dumps(a)
    s.sendto(a, server)
    toolbox.time.sleep(0.5)
    s.shutdown(socket.SHUT_RDWR)

if __name__=='__main__':
    Main()