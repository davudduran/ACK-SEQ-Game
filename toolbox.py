import time,inputimeout,random

DATALENGTH=10
TFMap = {'1':False,
         '2':True,
         't':True,
         'f':False,
         'y':True,
         'n':False,
         'no':False,
         'yes':True}

class Computer:
    def __init__(self,name='COMP',dl=DATALENGTH,autoMode=False):
        self.name=name
        self.dl=dl
        self.LastSentMessage = message(0,0,0,0) # to check values
        self.LastReceivedMessage = message(0,0,0,0)
        self.autoMode=autoMode
        self.points = 9999999

    def receiveMessage(self,m):
        print('\n'+self.name)
        if m.dl != 0:
            print(f"ReceivedMessage SEQ:{m.seq} ACK:{m.ack} DL:{m.dl}")
        #self.checkMessage(m)
        randResult = random.randint(0,4)
        if randResult==4: # BEN MESAJINI ALMADIM ACK ARTMAYACAK
            newm = message(m.ack,self.LastSentMessage.ack,self.dl, 0)
            self.losePoint()
        elif randResult==0 and not self.autoMode: # TIMEOUT ATCAK AFK TAKILCAK MESAJ YOK # SU AN CALISTIRAMADIGIMIZ ICIN COMMENT
            newm = None
        else:
            newm = message(m.ack, m.seq + m.dl, self.dl, 0)
        if newm != None:
            self.LastSentMessage=newm
            print(f"Sending Message SEQ:{newm.seq} ACK:{newm.ack} DL:{newm.dl}")
        self.LastReceivedMessage=m
        return newm
    
    def losePoint(self):
        self.points -= 1


class User:
    def __init__(self):
        self.LastSentMessage = message(0,0,10,0)
        self.LastReceivedMessage = message(0,0,0,0)
        self.initPoints()

    def timeout(self,sleep_time):
        time.sleep(sleep_time)
        try:
            response = TFMap.get(inputimeout.inputimeout(prompt='\nIs it time out?: ', timeout=15).strip().lower())
            if not response:
                print("It was timeout, you lost point.")
                self.losePoint()
        except inputimeout.TimeoutOccurred:
            print('Timeout span passed, you lost point.')
            self.losePoint()
        

    def initPoints(self):
        i = input("Point count: ").strip()
        try:
            int_i = int(i)

            if int_i < 1:
                print("Invalid count. Set to default points of 5.")
                self.points = 5
            else:
                self.points = int_i
        except ValueError:
            print("Invalid count. Set to default points of 5.")
            self.points = 5

    def receiveMessage(self,m):
        wrong = False
        if m != None:
            print(f"\nReceivedMessage SEQ:{m.seq} ACK:{m.ack} DL:{m.dl}")
            correctAnswer = message(self.LastSentMessage.ack,self.LastSentMessage.seq+self.LastSentMessage.dl,80, 0) # karsidan gelmesi gereken mesaj
            while True:
                isCorrect = TFMap.get(input('Is that response correct? Y\\N: ').strip().lower()) # Her cevaptan sonra True/False istedi hoca puan kontrolu icin 01:14:45'te
                if isCorrect is not None:
                    break
                print("Invalid answer.")
            if not isCorrect and correctAnswer.seq == m.seq and correctAnswer.ack == m.ack:
                print('Wrong, answer was correct.')
                self.losePoint()
            elif isCorrect and (correctAnswer.seq != m.seq or correctAnswer.ack != m.ack):
                print(f'Wrong, ',end='')
                if correctAnswer.seq != m.seq:
                    print(f"SEQ should be {correctAnswer.seq}. ",end='')
                if correctAnswer.ack != m.ack:
                    print(f'ACK was supposed to be {correctAnswer.ack}. ',end='')
                wrong=True
                print()
                self.losePoint()

        if self.points != 0:
            try:
                seq,ack,dl = map(int, [i.strip() for i in inputimeout.inputimeout(prompt='Enter SEQ ACK DL: ', timeout=60).strip().split(' ') if i.strip()])
                if m == None or wrong:
                    if seq != self.LastSentMessage.seq or ack != self.LastSentMessage.ack or dl != self.LastSentMessage.dl:
                        print("Wrong, the message should be the same with the last sent one.")
                        print(f'Sending message {self.LastSentMessage}')
                        self.losePoint()
                else: # Karsidan gelen mesaj dogruysa ona dogru cevap ver lan
                    expectedMessage = message(m.ack,m.seq+m.dl,self.LastSentMessage.dl,0)
                    if seq != expectedMessage.seq or ack != expectedMessage.ack:
                        print(f'You cannot send a message like that, you lost a point.')
                        print(f'Sending message {expectedMessage}')
                        self.LastSentMessage=expectedMessage
                        self.losePoint()
                    else:
                        self.LastSentMessage=message(seq,ack,dl,0)
                return self.LastSentMessage
            except inputimeout.TimeoutOccurred:
                print('Sorry, time is up. You lost a point.\nSending last message') # PUAN KAYBEDECEK
                print(f'Sending message {self.LastSentMessage}')
                self.losePoint()
                return self.LastSentMessage

    def losePoint(self):
        self.points -= 1
        print("Remaining points: {}".format(self.points))


class message:
    def __init__(self,seq,ack,dl,data):
        self.seq=seq
        self.ack=ack
        self.dl=dl
        self.data=data

    def __str__(self):
        return 'seq:{}ack:{}dl:{}data:{}'.format(self.seq,self.ack,self.dl,self.data)

if __name__=='__main__':
    c=Computer('TEST')