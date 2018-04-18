import socket

#Global variable for number of client connections
clients = 1

def server():
#Get host name
host = socket.gethostname()

#Initiate port to 5110
port = 55555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind host address and port
s.bind((host, port)

#Server can listen to one client only
server_socket.listen(clients)

#Accept connection
conn, address = server_socket.accept()

#while loop
while True:
	#Inputting packets no more than 2048 bytes in size
    data = server_socket.recvfrom(2048)

    if not data: break

    lowerData = data.lower()

    #Returning data to client in lowercase
    server_socket.send(lowerData)
