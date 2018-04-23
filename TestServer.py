import socket
import opencv_workspace/LaneTrackingNeuralNet as net

def Main():
    host = "159.89.53.176"
    port = 5000
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
            data = conn.recv(230400).decode()
			data = np.reshape(data, (1, 230400))
            if not data:
                    break
			message = net.neural_network_output(data)
            conn.send(message.encode())
             
    conn.close()
     
if __name__ == '__main__':
    Main()