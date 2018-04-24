#!/usr/bin/env python3

import optparse
import socket
import sys

# parse input args
parser = optparse.OptionParser()
parser.add_option("-i", dest="ip", type="str", default="127.0.0.1")
parser.add_option("-p", dest="port", type="int", default="12345")
(options, args) = parser.parse_args()

# act as the display in a Chromecast-esque demonstration
def display():

	l_sock = None
	connection = None
	try:

		# create a TCP socket on the IP address and port in options
		l_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		l_sock.bind((options.ip, options.port))

		# listen for a single connection at a time
		while True:

			# debug
			print("<listening for a new connection on %s:%d>" % (options.ip, options.port))

			# listen for a single connection at a time
			l_sock.listen(1)

			# accept the connection to receive a handle and an address
			connection, from_addr = l_sock.accept()

			# debug
			print("<accpted a connection from %s:%d>" % (from_addr[0], from_addr[1]))

			# print received input until the conditional break inside
			while True:

				# get at most 1 KiB of input
				received = connection.recv(1024)

				# closed connection returns a null reference
				if not received:
					# debug
					print("<connection closed>")

					# leave the inner loop
					break

				# show whatever was received without breaking the line
				sys.stdout.write(received.decode("utf-8"))
				sys.stdout.flush()

	# exit cleanly
	except Exception as ex:
		if connection is not None:
			connection.close()
		if l_sock is not None:
			l_sock.close()

		raise ex

if __name__ == "__main__":
	display()
