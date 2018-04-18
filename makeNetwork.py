#!usr/bin/python
from mininet.util import pmonitor
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.log import lg

def makeNetwork():
    
    #Create a simple network
    net = Mininet(SingleSwitchTopo(2), controller=OVSController)
    net.start()

    #Testing network
    print("Dumping hose connections...")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity...")
    net.pingAll()
    print("Testing bandwidth between client and server...")
    h1, h2 = net.get('h1', 'h2')
    net.iperf((h1, h2))
    
    CLI(net)

    h1 = net.get('h1')
    h1.cmd('python server.py -i %s &' % h1.IP())
    h2 = net.get('h2')
    h2.cmd('python client.py -i %s -m %s' % h1.IP(), message)

    #Terminate network
    net.stop()

if __name__ == "__main__":
    makeNetwork()


