import time
 
""" NOTLAR
    Packeti aldiktan sonra corrupted mi degil mi? Ona gore seq-ack
    paket ya gider ya gitmez, bit bozulmasi yok
    Pipelining yapilmayacak
    1dk bekle, timeout oldu tekrar yolla
"""

""" GEREKTIGINDE ACILACAK SU AN ISE YARAMIYORLAR
autoMode = True #Auto veya manual

# 5 puandan baslayacaklar, hata yapanin puani dusecek
CLIENTHEALTH=5
SERVERHEALTH=5
"""
DATALENGTH=10


def main():
    m = message(0,0,0)
    comp1=Computer('COMP1')
    comp2=Computer('COMP2',20)
    while True:
        m=comp1.receiveMessage(m)
        time.sleep(0.25)
        m=comp2.receiveMessage(m)
        time.sleep(0.25)

class Computer:
    def __init__(self,name='COMP',dl=DATALENGTH):
        self.name=name
        self.dl=dl
        LastSentMessage = message(0,0,0) # to check values

    def checkMessage(self,m):
        if m.dl != 0:
            print(f"ReceivedMessage SEQ:{m.seq} ACK:{m.ack} DL:{m.dl}")
        # eger son mesaj'ın seq+dl'si gelen mesajın ack'ine eşit değilse HATA VAR

    def receiveMessage(self,m):
        print('\n'+self.name)
        self.checkMessage(m)
        newm = message(m.ack, m.seq + m.dl, self.dl)
        self.LastSentMessage=newm
        print(f"Sending Message SEQ:{newm.seq} ACK:{newm.ack} DL:{newm.dl}")
        return newm

class User:
    def __init__(self):
        pass


class message:
    def __init__(self,seq,ack,dl):
        self.seq=seq
        self.ack=ack
        self.dl=dl
        #pcktlen random olabilir ya da fix secilebilir, şimdilik fixed

if __name__=='__main__':
    main()