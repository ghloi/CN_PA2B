from client import *
#Ask for important data 
serverIp=input('Enter the server IP address: ')
serverPort=int(input('Enter the server port number: '))
protocol=input('Enter protocol: ')
fileName=input('Enter file name: ')

#Create object of Client class and start process. 
clientStart=Client(serverIp, serverPort, protocol, fileName)

clientStart.recieve()