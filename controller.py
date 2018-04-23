#!usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.log import setLogLevel

def controller():

     parser = optparse.OptionParser()
     parser.add_option("-i", dest="ip", default="127.0.0.1")
     parser.add_option("-p", dest="port", type="int", default="12345")
     parser.add_option("-m", dest="msg")
     (options, args) = parser.parse_args()

     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.sendto(options.msg, (options.ip, options.port))
    
     print "\n"
     print "----------Welcome to TextCast-----------\n"
     print "Would you like to list the text files?\n"
     answer = input("Enter Yes(Y) or No (N)")

     temp=True

     while temp=True:
          if answer.lower=="n" or answer.lower=="no":
               break
          elif answer.lower=="y" or answer.lower=="yes":
               





          elif:
               print "\nWrong Input!\n"
               print "Would you like to list the text files?\n"
               answer = input("Enter Yes(Y) or No (N)")
	  


if __name__ == "__main__":
     controller()
