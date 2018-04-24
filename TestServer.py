import socket
import opencv_workspace/LaneTrackingNeuralNet as net
import os

def Main():
    host = "159.89.53.176"
    port = 5000
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        message = mySocket.recv(1024)
        file = open('message.npy', 'wb')
        while message:
            file.write(message)
            message = mySocket.recv(1024)
        print("Data Recieved")
		file.close()
		data = np.load('message.npy')
        message = net.neural_network_output(data)
        conn.send(message.encode())
        os.remove('message.npy')     
    conn.close()
     
if __name__ == '__main__':
    Main()