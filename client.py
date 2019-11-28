import socket
import sys
import random
import time
import struct

"""
Készítsünk egy barkóba alkalmazást. A szerver legyen képes kiszolgálni több klienst. A szerver válasszon egy egész számot 1..100 között véletlenszerűen. A kliensek próbálják kitalálni a számot.

    A kliens logaritmikus keresés segítségével találja ki a gondolt számot. AZAZ a kliens NE a standard inputról dolgozzon.
    Ha egy kliens kitalálta a számot, akkor a szerver minden újabb kliens üzenetre a „Vége” (V) üzenetet küldi, amire a kliensek kilépnek.
    Nyertél (Y), Kiestél (K) és Vége (V) üzenet fogadása esetén a kliens bontja a kapcsolatot és terminál. Igen (I) / Nem (N) esetén folytatja a kérdezgetést.
    A kommunikációhoz TCP-t használjunk!

Üzenet formátum:

    Klienstől: bináris formában egy db karakter, 32 bites egész szám. (struct) Ne használjuk a byte sorrend módosító operátort a struct-ban! (‘!’)
        A karakter lehet: <: kisebb-e, >: nagyobb-e, =: egyenlő-e
        pl: (‘>’,10)
    Szervertől: ugyanaz a bináris formátum , de a számnak nincs szerepe, bármi lehet (struct)
        A karakter lehet: I: Igen, N: Nem, K: Kiestél, Y: Nyertél, V: Vége
        pl: (‘V’,0)

Script paraméterezése:

    python3 client.py <hostname> <port szám>
        pl: python3 client.py localhost 10000
    python3 server.py <hostname> <port szám>
        pl: python3 client.py localhost 10000
"""

Hostname = sys.argv[1]
PortNum = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((Hostname,int(PortNum)))

Border = [1,100]
Operators = ["<",">"]
bGameIsRunning = True
while (bGameIsRunning):
    if(Border[0]==Border[1]):
        CurrentGuess = Border[0]
        OperatorGuess = '='
    else:
        CurrentGuess = random.randint(Border[0],Border[1])
        OperatorGuess = Operators[random.randint(0,1)]
    
    packer = struct.Struct('1s I')
    packed_data = packer.pack(OperatorGuess.encode(), CurrentGuess)
    sock.send(packed_data)
    print("Sent: "+OperatorGuess+str(CurrentGuess))
    PackedAnswer = sock.recv(1024)
    (EAnswer, TempNum) = packer.unpack(PackedAnswer)
    Answer = EAnswer.decode()
    print("Received: "+Answer)
    if (Answer == 'I'):
        if(OperatorGuess == '<'):
            Border[1] = CurrentGuess
        elif(OperatorGuess == '>'):
            Border[0] = CurrentGuess
    elif(Answer == 'N'):
        if(OperatorGuess == '<'):
            Border[0] = CurrentGuess
        elif(OperatorGuess == '>'):
            Border[1] = CurrentGuess
    elif(Answer == 'Y' or Answer == 'K' or Answer == 'V' ):
        bGameIsRunning = False
    print("The Number is between:"+str(Border[0])+"-"+str(Border[1]))
    time.sleep(random.randint(1,5))
print("Singing off")
sock.close()