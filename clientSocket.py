import socket
import main
import pickle

def Main():

    host=socket.gethostbyname(socket.gethostname()) #client ip
    port = 42451
    
    server = ('192.168.1.155', 42069)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    #autoMode = {'1':False,'2':True}.get(input("1. Manual\n2. Automatic\n\nPlease choose a game mode: "))
    c = main.Computer("ClientTest",10)
    m = main.message(0,0,10)
    while m !='q':
        #CREATE ANSWER pt2
        m = pickle.dumps(m)
        s.sendto(m, server)

        #GET MESSAGE
        data, addr = s.recvfrom(1024)
        data = pickle.loads(data)
        main.time.sleep(0.5)
        #CREATE ANSWER pt1
        m = c.receiveMessage(data)
    s.close()

if __name__=='__main__':
    Main()