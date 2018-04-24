#!/usr/bin/env python2

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

    temp = server.cmd('xterm -hold -e ./server.py -i %s &' % server.IP())
    temp = displayer.cmd('xterm -hold -e ./display.py -i %s &' % displayer.IP())
    temp = controller.cmd('xterm -hold -e ./controller.py -i %s --iface_display %s &' % (server.IP(), displayer.IP()))

    CLI(net)

    #Terminate network
    net.stop()

if __name__ == "__main__":
    startCast()


