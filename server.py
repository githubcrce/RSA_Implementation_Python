import socket
import time 

class RSA:
    def __init__(self):
        self.p = 239
        self.q = 263
        self.n = self.p * self.q
        self.totient = (self.p-1)*(self.q-1)
        self.privateKey = ""
        self.publicKey = 0


    def setPublicKey(self,publicKey):
        self.publicKey = publicKey        

    def getPublicKey(self):
        totient = self.totient
        i = 2
        while i < totient and i > 1:
            if self.gcd(i,totient) == 1:
                self.setPublicKey(i)
                publicKey = i
                break
            i += 1
        return totient, publicKey
    
    def egcd(self,a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self.egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
    def getPrivateKey(self,a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        return x % m
        

    def gcd(self,x,y):
        while(y):
            x, y = y, x % y
        return x

if __name__ == '__main__':
    port = 4999
    address = '127.0.0.1'
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((address,port))
    print("Listening on the port: ")
    s.listen(5)
    conn,addr = s.accept()
    print("connection established with : ",addr)
    Server = RSA()
    print("Prime Numbers Selected are: ",Server.p,Server.q)
    print("N is: ",Server.n)
    print("Totient is:",Server.totient)
    gen_st = time.time()
    totient, publicKey = Server.getPublicKey()
    privateKey = Server.getPrivateKey(publicKey,totient)
    if privateKey < 0: privateKey += Server.totient
    print("Public Key pair is(N,e): ",Server.n,publicKey)
    print("Private Key pair is(N,d):",Server.n,privateKey)
    time.sleep(0.004)
    gen_entime = time.time()
    print(f"rsa generation time : {(gen_entime-gen_st)}")
    messageToSend = str(publicKey) + ":" + str(Server.n)
    conn.send(messageToSend.encode('ASCII'))
    while True:
        data = conn.recv(1024).decode('ASCII')
        print("Message recieved was: ",data)
        print("**********Decrypting********")
        decrypt_starttime = time.time()
        if type(data):
            cipherText = int(data)
            privateKey = int(privateKey)
            plainText = (cipherText**privateKey) % Server.n
            print("PlainText was: ",plainText)
            decrypt_endtime = time.time()
            print(f"decryption time : {(decrypt_endtime-decrypt_starttime)}")
            break