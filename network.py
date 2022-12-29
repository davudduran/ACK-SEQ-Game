import time

autoMode = True #Auto veya manual

# 5 puandan baslayacaklar, hata yapanin puani dusecek
CLIENTHEALTH=5
SERVERHEALTH=5

DATALENGTH=10


def main():
    m = message(-1,0,0)
    while True:
        m = Client(m)
        m = ServerAuto(m)
        time.sleep(0.5)
        

#Computer - her zaman dogru yapacak, hata yok
def ServerAuto(m):
    """ 
    Packeti aldiktan sonra corrupted mi degil mi? Ona gore seq-ack
    paket ya gider ya gitmez, bit bozulmasi yok
    Pipelining yapilmayacak
    1dk bekle, timeout oldu tekrar yolla
    """
    print("\nSERVER SIDE")
    if m.dl != 0:
        print(f"Received Message SEQ:{m.seq} ACK:{m.ack} DL:{m.dl}")
    return message(m.ack,m.seq+1,DATALENGTH+10)


def ServerManual():
    #TO DO, user will control
    pass

def Client(m):
    print("\nCLIENT SIDE")
    if m.dl != 0:
        print(f"Received Message SEQ:{m.seq} ACK:{m.ack} DL:{m.dl}")
    newm = message(m.ack+m.dl,m.seq+1,DATALENGTH)
    print(f"Sending Message SEQ:{newm.seq} ACK:{newm.ack} DL:{newm.dl}")
    return newm

class message:
    def __init__(self,seq,ack,dl):
        self.seq=seq
        self.ack=ack
        self.dl=dl 
        #pcktlen random olabilir ya da fix secilebilir

if __name__=='__main__':
    main()