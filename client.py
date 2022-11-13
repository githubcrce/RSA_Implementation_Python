import socket
import os
from xmlrpc.client import Server
import time
if __name__ == '__main__':
    s = socket.socket()
    port=4999
    address='127.0.0.1'
    s= socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    #connecting server to socket(ip+portnumber)
    s.connect((address,port))
    recievedmessage = s.recv(1024).decode('ASCII')  #data is received
    ServerPublicKey, ServerN = recievedmessage.split(":")
    print("We recieved ServerPublicKey: ",ServerPublicKey)
    plainText = int(input("Enter plainText: "))
    print("********Encrypting*********")
    encrypt_starttime = time.time()
    cipherText = ((plainText)**int(ServerPublicKey)) % int(ServerN)
    print("CipherText generated is: ",cipherText)
    time.sleep(0.004)
    encrypt_endtime = time.time()
    print(f"encrption time : {(encrypt_endtime-encrypt_starttime)}")
    messageToSend = str(cipherText)
    print("Sent the message to client: ",messageToSend)
    s.send(messageToSend.encode('ASCII'))