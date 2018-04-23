#!usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.log import setLogLevel

def startCast():
    
    #Create a single switch network with 3 hosts
    net = Mininet(SingleSwitchTopo(k=3))
    
    net.start()

    controller = net.get('h1')
    displayer = net.get('h2')
    server = net.get('h3')

    temp = server.cmd('xterm')
    temp = displayer.cmd('xterm')
    temp = controller.cmd('xterm')

    CLI(net)
    
    #Terminate network
    net.stop()

if __name__ == "__main__":
    startCast()


