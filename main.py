import time
import sys
import inputimeout
import random
 
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
TFMap = {'1':False,
         '2':True,
         't':True,
         'f':False,
         'y':True,
         'n':False,}

def main(): # ISE YARAMAZ SU ANDA
    # 0 : Normal Messaging between computers
    # 1 : Computer wrong message check 55. satirda aciklama var
    # 2 : Computer wrong sequence check 58. satirda aciklama var
    testValue=2

    #init
    m = message(0,0,0,0)
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
        m=comp1.receiveMessage(message(0,0,1,0))
    elif testValue==2:
        m=comp1.receiveMessage(m)
        m=comp1.receiveMessage(message(5,5,10,0))

class Computer:

    def __init__(self,name='COMP',dl=DATALENGTH):
        self.name=name
        self.dl=dl
        self.LastSentMessage = message(0,0,0,0) # to check values
        self.LastReceivedMessage = message(0,0,0,0)
        self.seqError=False
        self.points = 1

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
        randResult = random.randint(0,4)
        if randResult==5: # BEN MESAJINI ALMADIM ACK ARTMAYACAK
            newm = message(m.ack,self.LastSentMessage.ack,self.dl, 0)
            self.losePoint()
        #elif randResult==9: # TIMEOUT ATCAK AFK TAKILCAK MESAJ YOK # SU AN CALISTIRAMADIGIMIZ ICIN COMMENT
        else:
            newm = message(m.ack, m.seq + m.dl, self.dl, 0)

        self.LastSentMessage=newm
        print(f"Sending Message SEQ:{newm.seq} ACK:{newm.ack} DL:{newm.dl}")
        self.LastReceivedMessage=m
        return newm
    
    def losePoint(self):
        self.points -= 1


class User:
    def __init__(self):
        self.LastSentMessage = message(0,0,0,0)
        self.LastReceivedMessage = message(0,0,0, 0)
        self.points = 1

    def receiveMessage(self,m):
        print(f"\nReceivedMessage SEQ:{m.seq} ACK:{m.ack} DL:{m.dl}")
        correctAnswer = message(self.LastSentMessage.ack,self.LastSentMessage.seq+self.LastSentMessage.dl,80, 0)
        isCorrect = TFMap.get(input('Is that response correct?Y\\N \n').lower()) # Her cevaptan sonra True/False istedi hoca puan kontrolu icin 01:14:45'te
        if isCorrect and correctAnswer.seq != m.seq:
            print(f"Wrong, sequence number should be {correctAnswer.seq}.")
            self.losePoint()
        if not isCorrect and correctAnswer.seq == m.seq and correctAnswer.ack == m.ack:
            print('Wrong, answer was correct')
            self.losePoint()
        elif isCorrect and correctAnswer.ack != m.ack:
            print(f'Wrong, ack was supposed to be {correctAnswer.ack}')
            self.losePoint()
        try:
            seq,ack,dl,syn = map(int, inputimeout.inputimeout(prompt='Enter Seq Ack Dl\nFormat: SS AA DD SYN: ', timeout=1500).split(' '))
            self.LastSentMessage=message(seq,ack,dl,0)
            return self.LastSentMessage
        except inputimeout.TimeoutOccurred:
            print('Sorry, times up') # PUAN KAYBEDECEK
            self.losePoint()
        else:
            pass

    def losePoint(self):
        self.points -= 1


class message:
    def __init__(self,seq,ack,dl,syn):
        self.seq=seq
        self.ack=ack
        self.dl=dl
        self.syn = 0 

    def __str__(self):
        return 'seq:{}ack:{}dl:{}syn:{}'.format(self.seq,self.ack,self.dl,self.syn)

if __name__=='__main__':
    c=Computer('TEST')