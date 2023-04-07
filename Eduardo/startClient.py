from client import *
serverIp=input('Enter the server IP address: ')
serverPort=int(input('Enter the server port number: '))
protocol=input('Enter protocol: ')
fileName=input('Enter file name: ')

clientStart=Client(serverIp, serverPort, protocol, fileName)

clientStart.recieve()