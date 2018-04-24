#! /usr/bin/env python3

# utilty to test the display script (not for submission)

import optparse
import socket
import time

# parse input args
# ammo is a string with the characters to send to the display
parser = optparse.OptionParser()
parser.add_option("-i", dest="ip", type="str", default="127.0.0.1")
parser.add_option("-p", dest="port", type="int", default="12345")
parser.add_option("-d", dest="delay_ms", type="int", default="100")
parser.add_option("-a", dest="ammo", type="str", default="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*()_+-=\n")
(options, args) = parser.parse_args()

def cannon():

	try:
		out_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		out_sock.connect((options.ip, options.port))

		while True:
			for c in options.ammo:
				out_sock.send(c.encode("utf-8"))
				time.sleep(options.delay_ms/1000.0)

	# catch ctrl-c to quit
	except KeyboardInterrupt:
		out_sock.close()

if __name__ == "__main__":
	cannon()