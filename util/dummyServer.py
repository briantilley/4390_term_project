#! /usr/bin/env python3

# utility to test the controller index request (not for submission)

import socket
import optparse

fake_index = "aaa\nbbb"#"file.txt\nsomething_else.zip\nimage.png\n1234567890\nnot_a_string.file\n"
request = "REQUEST INDEX"

# parse input args
parser = optparse.OptionParser()
parser.add_option("-i", dest="ip", type="str", default="127.0.0.1")
parser.add_option("-p", dest="port", type="int", default="12345")
(options, args) = parser.parse_args()

def dummyServer():

	sock = None
	try:

		sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		sock.bind((options.ip, options.port))

		while True:

			print("<listening for a new connection on %s:%d>" % (options.ip, options.port))

			sock.listen(1)

			conn, client = sock.accept()

			print("<accpted a connection from %s:%d>" % client)

			# listen for request
			while True:

				# get at most 1 KiB of input
				received = conn.recv(1024)

				# closed connection returns a null reference
				if not received:
					# debug
					print("<connection closed>")

					# leave the inner loop
					break

				message = received.decode("utf-8")

				print(message)

				if message == request:

					print("<sending index>")

					conn.send(fake_index.encode("utf-8"))
					conn.send(("END OF REPLY").encode("utf-8"))

	except Exception as e:

		if sock is not None:
			sock.close()

		raise e

if __name__ == "__main__":
	dummyServer()
