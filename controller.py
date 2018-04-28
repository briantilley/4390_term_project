#!/usr/bin/env python3

import optparse
import socket
import time
import sys

# custom module to play a file in a thread
from fileplay import play, pause, resume, stop

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

# Defining a "page" as 8 consecutive lines of text, send a page
# prepended with enough whitespace to clear the console.
def send_page(source_text, page_num, display_socket):

     # extract a single page
     page = ""
     lines_seen = 0
     for c in source_file:
          if lines_seen >= page_num * 8:
               page += c

          if c == '\n':
               lines_seen += 1

          if lines_seen >= (page_num + 1) * 8:
               break

     # trailing newline
     if page[-1] == '\n':
          page = page[:-1]

     # prepend whitespace
     message = '\n' * 100 + page

     # send
     display_socket.send(message)

def controller():

     # command line options passed in by startCast.py
     parser = optparse.OptionParser()
     parser.add_option("-i", dest="ip", type="str", default="127.0.0.1")
     parser.add_option("--iface_display", dest="ip_display", type="str", default="127.0.0.1")
     parser.add_option("-p", dest="port", type="int", default="12345")
     (options, args) = parser.parse_args()

     # create TCP sockets to talk to other hosts
     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     display_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

     # wait for other hosts to come online
     time.sleep(1)

     # connect to other hosts
     server_socket.connect((options.ip, options.port))
     display_socket.connect((options.ip_display, options.port))

     print("\n")
     print("----------Welcome to TextCast-----------\n")
     print("Would you like to list the text files?\n")
     answer = input("Enter Yes(Y) or No (N)")
     print("")

     temp=True

     while temp == True:
          if answer.lower()=="n" or answer.lower()=="no":
               break
          elif answer.lower()=="y" or answer.lower()=="yes":
               index = get_index(server_socket)

               desiredFiles = input("\nWhich files would you like to view?\nEnter files as comma separated list\n").split(",")
			   
               for file in desiredFiles:
                    message = file.strip() + " REQUEST FILE"
                    msgRequest = message.encode("utf-8")
                    server_socket.send(msgRequest)

                    msgReply = ""
                    while True:
                         fromServer = server_socket.recv(1024)
                         if not fromServer:
                              return None
          
			 # decode and append for processing
                         msgReply += fromServer.decode("utf-8")

                         # look for "end of reply" tag in the case of a long index
                         len_eor = len("END OF REPLY")

                         # debug
                         #print("<received \"%s\">" % (fromServer.decode("utf-8")))
			 play(fromServer.decode("utf-8"), display_socket)

                         # check for end of reply
                         if msgReply[-len_eor:] == "END OF REPLY":
                              msgReply = msgReply[:-len_eor]
                              break
                    
                    keep_going = True
                    while keep_going:
                         cmd = input("(p)ause, (r)esume, (s)top: ")[0].lower()
                         if 'p' == cmd:
                              pause()
                         elif 'r' == cmd:
                              resume()
                         elif 's' == cmd:
                              stop()
                              keep_going = False
                         else:
                              print("wot")
                    break

          else:
               print("\nWrong Input!\n")
               
          print("\nWould you like to list the text files?\n")
          answer = input("Enter Yes(Y) or No (N)")
          

if __name__ == "__main__":
     controller()
