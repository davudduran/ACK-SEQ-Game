import socket
import main
import pickle

def Main():

    host = socket.gethostbyname(socket.gethostname()) #Server ip
    port = 42069

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    c = main.Computer('Server',77)
    print("Server Started\nWaiting for client to start conversation.")
    while True:
        #GET MESSAGE
        data, addr = s.recvfrom(1024)
        data = pickle.loads(data)
        print("From: " + str(addr))
        main.time.sleep(0.5)
        #CREATE ANSWER
        m = c.receiveMessage(data)
        m = pickle.dumps(m)
        s.sendto(m, addr)
    s.close()

if __name__=='__main__':
    Main()