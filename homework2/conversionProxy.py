# CS 6421 - Simple Message Board Client in Python
# T. Wood
# Run with:     python msgclient.py

import socket
import sys

BUFFER_SIZE = 1024
interface = ""

ouncesDollarsHost = "localhost"
ouncesDollarsPort = 5555

dollarsYenHost = "localhost"
dollarsYenPort = 6666

def convert(unit, userInput):
    if unit == "ounces":
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((ouncesDollarsHost, ouncesDollarsPort))
        print clientsocket.recv(BUFFER_SIZE)
        clientsocket.send("ounces dollars " + userInput + "\n")
        result = clientsocket.recv(BUFFER_SIZE)

        clientsocket.close()
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((dollarsYenHost, dollarsYenPort))
        print clientsocket.recv(BUFFER_SIZE)
        clientsocket.send("dollars yen " + str(result) + "\n")
        return float(clientsocket.recv(BUFFER_SIZE))
        
    elif unit == "yen":
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((dollarsYenHost, dollarsYenPort))
        print clientsocket.recv(BUFFER_SIZE)
        clientsocket.send("yen dollars " + str(userInput) + "\n")
        result = clientsocket.recv(BUFFER_SIZE)
         
        clientsocket.close()
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((ouncesDollarsHost, ouncesDollarsPort))
        print clientsocket.recv(BUFFER_SIZE)
        clientsocket.send("dollars ounces " + result + "\n")
        return float(clientsocket.recv(BUFFER_SIZE))

## Function to process requests
def process(conn):
    conn.send("Welcome to the ounces of bananas/yen converter!\n")

    # read userInput from client
    userInput = conn.recv(BUFFER_SIZE)
    if not userInput:
        print "Error reading message"
        sys.exit(1)

    inputList = userInput.split(" ")
    
    if len(inputList) < 3: 
        conn.send("Not enough input!\n")
        conn.close()
        return
    
    if inputList[0] == "ounces" and inputList[1] != "yen":
        conn.send("Invalid input!\n")
        conn.close()
        return
        
    if inputList[0] == "yen" and inputList[1] != "ounces":
        conn.send("Invalid input!\n")
        conn.close()
        return

    result = convert(inputList[0], inputList[2])
        
    print "Received message: ", userInput
    
    conn.send(str(result) + "\n")

    conn.close()

# if input arguments are wrong, print out usage
if len(sys.argv) != 2:
    print >> sys.stderr, "usage: python {0} portnum\n".format(sys.argv[0])
    sys.exit(1)

portnum = int(sys.argv[1])

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((interface, portnum))
s.listen(5)

while True:
    # accept connection and print out info of client
    conn, addr = s.accept()
    print 'Accepted connection from client', addr
    process(conn)
s.close()