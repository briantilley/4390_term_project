import socket, optparse

#Parsing command
parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=55555)
parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

#Get instance of socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Send through socket
client_socket.sendto(options.msg, (options.ip, options.port))