import socket

def Main():

    host = socket.gethostbyname(socket.gethostname()) #Server ip
    port = 42069

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")
    while True:
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("From: " + str(addr))
        print("Message: " + data)
        data = input("-> ")
        #print("Sending: " + data)
        s.sendto(data.encode('utf-8'), addr)
    c.close()

if __name__=='__main__':
    Main()