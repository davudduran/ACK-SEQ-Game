import time
import re
 
""" NOTLAR
    Packeti aldiktan sonra corrupted mi degil mi? Ona gore seq-ack
    paket ya gider ya gitmez, bit bozulmasi yok
    Pipelining yapilmayacak
    1dk bekle, timeout oldu tekrar yolla
"""

""" GEREKTIGINDE ACILACAK SU AN ISE YARAMIYORLAR
# 5 puandan baslayacaklar, hata yapanin puani dusecek
CLIENTHEALTH=5
SERVERHEALTH=5
"""
DATALENGTH=10


def main():
    # 0 : Normal Messaging between computers
    # 1 : Computer wrong message check 55. satirda aciklama var
    # 2 : Computer wrong sequence check 58. satirda aciklama var
    testValue=2

    #init
    m = message(0,0,0)
    comp1=Computer('COMP1')
    comp2=Computer('COMP2',20)

    if testValue==0:
        while True:
            m=comp1.receiveMessage(m)
            time.sleep(0.25)
            m=comp2.receiveMessage(m)
            time.sleep(0.25)
    elif testValue==1:
        m=comp1.receiveMessage(m)
        m=comp1.receiveMessage(message(0,0,1))
    elif testValue==2:
        m=comp1.receiveMessage(m)
        m=comp1.receiveMessage(message(5,5,10))

class Computer:
    def __init__(self,name='COMP',dl=DATALENGTH):
        self.name=name
        self.dl=dl
        self.LastSentMessage = message(0,0,0) # to check values
        self.LastReceivedMessage = message(0,0,0)
        self.seqError=False

    def checkMessage(self,m):
        if m.dl != 0:
            print(f"ReceivedMessage SEQ:{m.seq} ACK:{m.ack} DL:{m.dl}")
        """if self.LastSentMessage.seq+self.LastSentMessage.dl != m.ack: # eger son gonderdigim mesajın seq+dl'si gelen mesajın ack'ine eşit değilse GIDEMEMIS VEYA HATA YAPILMIS
            print(f"Received ack:{m.ack}. Should be:{self.LastSentMessage.seq+self.LastSentMessage.dl}")
            self.seqError=True
        if self.LastSentMessage.ack != m.seq: # Gonderdigim ack'e gelen seq cevabi yanlis. -> Karsinin puanini dusurucek
            print(f"Sent ack:{self.LastSentMessage.ack} not equal to received seq:{m.seq}")"""
        

    def receiveMessage(self,m):
        print('\n'+self.name)
        self.checkMessage(m)
        if not self.seqError: # error yoksa yeni mesaji yolla
            newm = message(m.ack, m.seq + m.dl, self.dl)
        else: # yanlis geldiyse eski mesajda gitmesi gereken seq ve dl'i tekrar yolla
            newm = message(self.LastSentMessage.seq,m.seq+m.dl,self.LastSentMessage.dl)
        self.LastSentMessage=newm
        print(f"Sending Message SEQ:{newm.seq} ACK:{newm.ack} DL:{newm.dl}")
        return newm

    def stringToMessage(self,s):
        seq=re.findall('(?<=q:)\d+',s)[0]
        ack=re.findall('(?<=k:)\d+',s)[0]
        dl =re.findall('(?<=l:)\d+',s)[0]
        return message(seq,ack,dl)

class User:
    def __init__(self):
        pass


class message:
    def __init__(self,seq,ack,dl):
        self.seq=seq
        self.ack=ack
        self.dl=dl
        #pcktlen random olabilir ya da fix secilebilir, şimdilik fixed

    def __str__(self):
        return 'seq:{}ack:{}dl:{}'.format(self.seq,self.ack,self.dl)

if __name__=='__main__':
    c=Computer('TEST')
    c.stringToMessage('seq:30ack:25dl:10')