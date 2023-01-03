import socket,toolbox,pickle

def Main():

    host = socket.gethostbyname(socket.gethostname()) #Server ip
    port = 42069

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    c = toolbox.Computer('Server',77,True)
    print("Server Started\nWaiting for client to start conversation.")
    while True:
        #GET MESSAGE
        data, addr = s.recvfrom(1024)
        data = pickle.loads(data)
        #print("\nFrom: " + str(addr))
        toolbox.time.sleep(0.5)

        if data.data == 1:
            print("User lost.")
            break

        #CREATE ANSWER
        m = c.receiveMessage(data)
        m = pickle.dumps(m)
        s.sendto(m, addr)

    s.shutdown(socket.SHUT_RDWR)

if __name__=='__main__':
    Main()