#!/usr/bin/env python3

# from mininet.topo import Topo
# from mininet.net import Mininet
# from mininet.util import dumpNodeConnections
# from mininet.topo import SingleSwitchTopo
# from mininet.cli import CLI
# from mininet.node import OVSController
# from mininet.log import setLogLevel
import optparse
import socket

# return a list guaranteed not to have empty strings at the end
def trim_empty_strings(str_list):

     idx_last = -1
     last = str_list[-1]
     while last == '' and -idx_last <= len(str_list):
          idx_last -= 1
          last = str_list[idx_last]

     return str_list[ : idx_last % len(str_list) + 1]

# return a list of strings (filenames) from the server at the other end of the socket
# expects server to return a list of strings separated by newlines
def get_index(sock):

     # send an index request to the file server
     req = ("REQUEST INDEX").encode("utf-8")
     sock.send(req)

     # collect arbitrary number of responses into an index string
     index_str = ""
     while True:

          # listen for response
          response = sock.recv(1024)

          # socket was closed, return null ref.
          if not response:
               return None

          # decode and append for processing
          index_str += response.decode("utf-8")

          # look for "end of reply" tag in the case of a long index
          len_eor = len("END OF REPLY")

          # debug
          print("<received \"%s\">" % (response.decode("utf-8")))

          # check for end of reply
          if index_str[-len_eor:] == "END OF REPLY":

               # trim delimiter and quit
               index_str = index_str[:-len_eor]
               break

     # turn into a list
     return trim_empty_strings(index_str.split("\n"))

def controller():

     parser = optparse.OptionParser()
     parser.add_option("-i", dest="ip", default="127.0.0.1")
     parser.add_option("-p", dest="port", type="int", default="12345")
     # parser.add_option("-m", dest="msg")
     (options, args) = parser.parse_args()

     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((options.ip, options.port))

     print("\n")
     print("----------Welcome to TextCast-----------\n")
     print("Would you like to list the text files?\n")
     answer = input("Enter Yes(Y) or No (N)")

     temp=True

     while temp == True:
          if answer.lower()=="n" or answer.lower()=="no":
               break
          elif answer.lower()=="y" or answer.lower()=="yes":
               index = get_index(s)
               print(index)
               break




          else:
               print("\nWrong Input!\n")
               print("Would you like to list the text files?\n")
               answer = input("Enter Yes(Y) or No (N)")



if __name__ == "__main__":
     controller()
