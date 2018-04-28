#! /usr/bin/env python3

import socket
import optparse
import subprocess as sproc

# parse input args
parser = optparse.OptionParser()
parser.add_option("-i", dest="ip", type="str", default="127.0.0.1")
parser.add_option("-p", dest="port", type="int", default="12345")
parser.add_option("-c", dest="content_dir", type="str", default="content/") # directory for "media"
(options, args) = parser.parse_args()

# controller sends this message on its own to get the index
REQUEST_INDEX = "REQUEST INDEX"
REQUEST_FILE = "REQUEST FILE"

# return a string with the names of all content files separated by newlines
def get_index_str():

	global options

	# just get output from ls
	return sproc.run(["ls", "-1", options.content_dir], stdout=sproc.PIPE).stdout.decode("utf-8")

# split the index string and return as a list without trailing empty strings
def get_index_list():

	as_string = get_index_str()
	as_list = as_string.split("\n")
	while as_list[-1] == '':
		as_list = as_list[:-1]

	return as_list

def server():

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

				# get the message as a string
				message = received.decode("utf-8")

				# send index if requested
				if message == REQUEST_INDEX:

					# debug
					print("<sending index>")

					connection.send((get_index_str() + "END OF REPLY").encode("utf-8"))

				# send file if requested
				elif message[-len(REQUEST_FILE):] == REQUEST_FILE:

					# debug
					print("<received file request>")

					filename = message[:-len(REQUEST_FILE + " ")]
					index = get_index_list()
					if filename not in index:

						#debug
						print("<file not found>")

						connection.send("ERROR FILE NOT FOUND")

						# listen for next request
						continue

					# open the file, read as a string, and send through the connection
					with open(options.content_dir + filename, "r") as f:
						file_as_string = f.read()
						connection.send((file_as_string + "END OF REPLY").encode("utf-8"))

				# unknown
				else:

					# debug
					print("<received unknown message \"%s\">" % message)

					connection.send(("ERROR NOT RECOGNIZED").encode("utf-8"))

	# exit cleanly
	except Exception as ex:
		if connection is not None:
			connection.close()
		if l_sock is not None:
			l_sock.close()

		raise ex

if __name__ == "__main__":
	server()
