import socket
import main
import pickle

def Main():

    host=socket.gethostbyname(socket.gethostname()) #client ip
    port = 42451
    server = ('192.168.2.125', 42069)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    autoMode = main.TFMap.get(input("1. Manual\n2. Automatic\n\nPlease choose a game mode: "))
    if autoMode:
        c = main.Computer("ClientAuto",10)

    else:
        c = main.User()

    m = main.message(0,0,0,0)
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
        
        if c.points == 0:
            print("User lost.")
            c.points = 5
            a = main.message(0, 0, 0, 1)
            a = pickle.dumps(a)
            s.sendto(a, server)
            if data.syn == 1 and c.points == 0:
                break
    s.shutdown(socket.SHUT_RDWR)

if __name__=='__main__':
    Main()