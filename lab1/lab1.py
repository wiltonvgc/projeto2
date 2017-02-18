#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, info, setLogLevel
from mininet.util import dumpNodeConnections, quietRun, moveIntf
from mininet.cli import CLI
from mininet.node import Switch, OVSKernelSwitch

from subprocess import Popen, PIPE, check_output
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os
import termcolor as T
import time


class Topologia(Topo):
   
    def __init__(self):
        super(Topologia, self ).__init__()
        n1 = self.addNode('pc1')#host pc1
	n2 = self.addNode('pc2')#host pc2
	s0 = self.addSwitch('s0')#switch
	self.addLink(n1,s0)#link pc1 to s0
	self.addLink(n2,s0)#link pc2 to s0
	r0 = self.addSwitch('r0',type='Router')#roteador r0
	self.addLink(r0,s0)#link switch to router
	return

#Retorna IP de hosts	
def getIP(host):
	if(host=='pc1'):
		return '192.168.0.1/24'
	elif(host=='pc2'):
		return '192.168.0.2/24'
	elif(host=='r0'):
		return '192.168.0.254/24'

def main():
    os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")	

    net = Mininet(topo=Topologia())
    net.start()

    #Seta roteador r0
    for router in net.switches:
	if(router.name=='r0'):
        	router.cmd("sysctl -w net.ipv4.ip_forward=1")
        	router.waitOutput()

    #Configura interface do roteador r0 com zebra
    for router in net.switches:
        if(router.name == 'r0'):
       		router.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
        	router.waitOutput()

    #Configura interfaces dos hosts
    for host in net.hosts:
	host.cmd("ifconfig %s-eth0 %s" % (host.name, getIP(host.name)))
    	host.cmd("route add default gw %s" % '192.168.0.254')
    
    CLI(net)
    net.stop()
   


if __name__ == "__main__":
    main()
