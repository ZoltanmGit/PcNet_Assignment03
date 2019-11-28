import socket
import struct
import select
import random
import sys

def CheckNumber(argGameNumber, argGuessNumber, argGuessOperator):
    Answer = 'T'
    if (not bGameWon):
        if((argGuessNumber > argGameNumber and argGuessOperator == '>') or (argGuessNumber < argGameNumber and argGuessOperator == '<') or (argGuessNumber == argGameNumber and argGuessOperator != '=')):
            Answer = 'N'
        elif((argGuessNumber > argGameNumber and argGuessOperator == '<') or (argGuessNumber < argGameNumber and argGuessOperator == '>' )):
            Answer = 'I'
        elif(argGuessNumber == argGameNumber and argGuessOperator == '='):
            Answer = 'Y'
        elif(argGuessNumber != argGameNumber and argGuessOperator == '='):
            Answer = 'K'
        return Answer
    else:
        Answer = 'V'
        return Answer

Hostname = sys.argv[1]
PortNum = sys.argv[2]
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sock.bind((Hostname,int(PortNum)))
serv_sock.listen(10)


#bClients = True
inputs = [serv_sock]
clients = []
while True:
    if(clients == []):
        GameNumber = random.randint(1,100)
        bGameWon = False
        print ("The Number is: "+str(GameNumber))
    readable, _ , _ = select.select(inputs,[],[])
    for s in readable:
        if s is serv_sock:
            new_cient, cli_addr = s.accept()
            print('NEW CLIENT: ' + str(cli_addr))
            inputs.append(new_cient)
            clients.append(new_cient)
        else:
            packer = struct.Struct('1s I')
            packed_data = s.recv(1024)
            if packed_data:
                (Op, Guess) = packer.unpack(packed_data)
                print("Received: "+Op.decode()+str(Guess))
                Reply = CheckNumber(GameNumber, Guess, Op.decode())
                packed_reply = packer.pack(Reply.encode(), 1)
                if(Reply == 'Y'):
                    bGameWon = True
                s.send(packed_reply)
                print("Sent: "+Reply)
            else:
                inputs.remove(s)
                clients.remove(s)
serv_sock.close()