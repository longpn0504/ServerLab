# Import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 80  # Port number
serverSocket.bind(('10.32.141.179', serverPort))
serverSocket.listen(1)

print('The server is ready to receive requests...')

while True:
    # Establish the connection
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send HTTP response header
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'.encode())

        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()
