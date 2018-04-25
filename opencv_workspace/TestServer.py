import socket
import LaneTrackingNeuralNet as net
import os
import numpy as np

def Main():
    host = "159.89.53.176"
    port = 4008

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        message = conn.recv(1024)
        file = open('message.npy', 'wb')
        for i in range(320):
            file.write(message)
            if i == 309:
               break
            message = conn.recv(1024)
            print(message)
        print("Data Recieved")
        file.close()
        data = np.load('message.npy')
        message = net.neural_network_output(data)
        conn.send(message.encode())
        os.remove('message.npy')     
    conn.close()


if __name__ == '__main__':
    Main()
