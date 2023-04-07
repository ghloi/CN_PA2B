#   This program was made by Gregorio Loi on March 26, 2023
#   Intended use was for Programming Assignment 2 Submission for Computer Networks

import sys, os, select, time, socket

import udt, packet #HELPER MODULES
from timer import Timer #Helper Timer Class

#       HELPER FUNCTIONS
def getInteger(displayMessage):
    inputInt = False
    while inputInt==False:
        try:
            inputInt = int(input(displayMessage))
        except Exception as e:
            #Error occured, display error and retry (While Loop)
            print("Error Integer Input: "+str(e))
            inputInt = False
    
    return inputInt

def getReceiverIP():
    inputIP = False
    while inputIP==False:
        try:
            inputIP = str(input("Provide Receiver IP: "))
            #Verification optional
        except Exception as e:
            #Error occured, display error and retry (While Loop)
            print("Error IP Input: "+str(e))
            inputIP = False
    
    return inputIP

def getWindowSize():
    winSize = False
    while winSize==False:
        try:
            winSize = int(input("Enter Window Size (N): #"))
        except Exception as e:
            #Error occured, display error and retry (While Loop)
            print("Error Window Size (N) Input: "+str(e))
            winSize = False
    
    return winSize

#       HELPER FUNCTIONS
def getProtocol():
    inputProtocol = False
    while inputProtocol==False:
        try:
            inputProtocol = int(input("Choose a protocol:\n1. [SnW]\n2. [GBN]\nEnter your choice (1-2): "))
            if (inputProtocol != 1) and (inputProtocol != 2):
                print("Invalid selection! Choose between 1 [SnW] or 2 [GBN].")
                inputProtocol = False
        except Exception as e:
            #Error occured, display error and retry (While Loop)
            print("Error Protocol Input: "+str(e))
            inputProtocol = False
    if inputProtocol == 1:
        return "SnW"
    return "GBN"

def startServer(inputPort):
    # The proxy server is listening at inputPort 
    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET for IPv4 and SOCK_STREAM for TCP
    tcpSerSock.setblocking(1) #Sets blocking to true (1), which means code will yield for sockets
    tcpSerSock.bind(('localhost', inputPort))
    tcpSerSock.listen(100) #Number inside listen() is maximum number of queued connections allowed

    #List of Sockets to monitor
    socketList = [tcpSerSock]

    #Let's start
    while socketList:
        # Strat receiving data from the client
        readable, writable, exceptional = select.select(socketList, [], [])

        #GO THROUGH EACH READABLE FILE DESCRIPTOR
        for sock in readable:
            if sock is tcpSerSock:
                #Accept a new connection and add that new connection to list of inputs
                clientsock, addr = tcpSerSock.accept()
                print('Connection accepted from '+str(addr[0]))
                socketList.append(clientsock)
            else:
                data = sock.recv(1000) #TCP Payload
                #Send 1000 and receive 1000
                if not data:
                    #Close connections one of the sockets disconnected
                    print("Connection closed, See you later!")
                    print(" ")
                    print("*****************************************************************************") #NewLine
                    print('Listening for connection at Port '+str(inputPort)+'...')
                    print("*****************************************************************************") #NewLine

                    #Current Socket Removal
                    sock.close()
                    if sock in socketList:
                        socketList.remove(sock)
                    continue #Stop here
                
                #File Name and File Path Variables
                fileName = str(data)
                filePath = "./Server/"+str(data)

                #Check if file exists, otherwise send an error
                print("Asking for file: "+fileName)
                if not os.path.exists(filePath):
                    print("File Not Found! Sending error ...")
                    sock.send("Error404EOF") #File Not Found
                    print("Error Message Sent!")
                else:
                    print("Sending the file ...")
                    fileObj = open(filePath, 'rb')
                    while True:
                        fileChunk = fileObj.read(1000)
                        if not fileChunk:
                            break #End of File
                        #Send the FileChunk
                        sock.send(fileChunk)
                    #Done transferring
                    print("Transfer Complete!")
                    sock.send("EOF")

                
                #sock.sendall("EOF") #Signal we're done sending data!

    tcpSerSock.close()


def send_snw(inputPort, clientIP, clientPort, timeout):
    #Important Variables
    clientAddress = (clientIP, clientPort)
    bufferSize = 999 #Save 1 byte for sequence number
    seqNum = 0 #Start at 0
    fileName = 'mickey.png'
    DEFAULT_FILE = open(fileName, 'rb') #Default File hardcoded
    fileSize = os.path.getsize(fileName)
    timerObj = Timer(timeout)

    #Create our UDP Socket first for Server to listen on
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', inputPort))

    #Go through entire file in bufferSize increments
    for i in range(0, fileSize, bufferSize):
        #Get a chunk of data from file
        dataChunk = DEFAULT_FILE.read(bufferSize)

        ackReceived = False
        while not ackReceived:
            #Create a packet
            dataPacket = packet.make(seqNum, dataChunk)

            #Send it
            sock.send(dataPacket, sock, clientAddress)

            #NOW WE TIMEOUT AND RECEIVE
            timerObj.start() #Start the timer
            while not timerObj.timeout():
                #Iteratively try to get an ACK signal
                try:
                    sock.settimeout(0.1) #VERY SHORT TIMEOUT
                    rcvPacket = sock.recvfrom(bufferSize)
                    rcvSeqNum, rcvData = packet.extract(rcvPacket)
                    if rcvSeqNum == seqNum:
                        #We received our seq num!! Yay
                        ackReceived = True #To break while loop
                        seqNum = 1 - seqNum #Sets 1 to 0, 0 to 1
                        break
                except Exception as e:
                    #Ignore this branch of code, only used to catch socket timing out every 0.1 seconds
                    pass
            
            #Now, check if Acknowledgement was received (Packet sent successfully)
            if not ackReceived:
                print("Acknowledgement not received - Retransmitting packet!")
            timerObj.stop() #For next time use

    sock.sendto('EOF', clientAddress) #END OF FILE TRANSMISSION DONE
    print('File Transfer complete! Closing socket.')
    sock.close()
            







#       MAIN
def main():
    #Get Input Port Number for server listening on
    inputPort = getInteger("Provide Port for incoming connections: #") #Integer Port Number

    #Get Input IP Address to send file to
    clientIP = getReceiverIP()
    clientPort = getInteger("Provide Receiver Port: #") #Integer Port Number

    #Get Input Protocol for sending file
    inputProtocol = getProtocol() #String "SnW" or "GBN"

    #If GBN, get Window Size!
    if inputProtocol == "GBN":
        windowSize = getWindowSize()
    else:
        timeout = getInteger("Enter timeout for packets in seconds: ")

    #Print Messages for Debug
    print('Sending file to '+str(clientIP)+':'+str(clientPort)+'...')
    print('Using Protocol: '+str(inputProtocol))
    if inputProtocol == "GBN":
        print('Window Size (N) is: '+str(windowSize))
    else:
        print('Packet timeout in seconds is: '+str(timeout))
    print("*****************************************************************************") #NewLine

    # #Let's listen on it >:)
    # startServer(inputPort)
    if inputProtocol == "GBN":
        print("Sending with GBN...")
    else:
        print("Sending with SnW...")
        send_snw(inputPort, clientIP, clientPort, timeout)



if __name__ == "__main__":
    main()