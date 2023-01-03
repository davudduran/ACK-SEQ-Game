import socket
import time
import toolbox
import pickle
import select

def Main():

    host=socket.gethostbyname(socket.gethostname()) #client ip
    port = 42451
    server = ('192.168.1.137', 42069)
    lastSentMessageTime = time.time()
    time_since = time.time()-lastSentMessageTime
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    ready = select.select([s],[],[],0.1)
    s.setblocking(0)
    autoMode = toolbox.TFMap.get(input("1. Manual\n2. Automatic\n\nPlease choose a game mode: "))
    if autoMode:
        c = toolbox.Computer("ClientAuto",10)

    else:
        c = toolbox.User()

    m = toolbox.message(0,0,0,0)
    m = pickle.dumps(m)
    s.sendto(m,server)
    timeout = False
    while c.points != 0:
        #CREATE ANSWER pt2
        if ready[0] or timeout:
            timeout = False
            m = pickle.dumps(m)
            lastSentMessageTime=time.time()
            time_since=0
            s.sendto(m, server)
            
        #GET MESSAGE
        ready = select.select([s],[],[],0.5)
        if ready[0]:
            data, addr = s.recvfrom(1024)
            data = pickle.loads(data)

            if data == None:
                time.sleep(5)
            
            time_since=time.time()-lastSentMessageTime
            if time_since>5:
                m = c.timeout()
                timeout = True

            m = c.receiveMessage(data)
        
    print("User lost.")
    a = toolbox.message(0, 0, 0, 1)
    a = pickle.dumps(a)
    s.sendto(a, server)
    toolbox.time.sleep(0.5)
    s.shutdown(socket.SHUT_RDWR)

if __name__=='__main__':
    Main()