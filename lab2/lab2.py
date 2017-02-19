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
	
	#Criacao dos hosts
        pc11 = self.addNode('pc11')#host pc1.1
	pc12 = self.addNode('pc12')#host pc1.2
	pc21 = self.addNode('pc21')#host pc2.1
	pc22 = self.addNode('pc22')#host pc2.2
	pc31 = self.addNode('pc31')#host pc3.1
	pc32 = self.addNode('pc32')#host pc3.2
	pc81 = self.addNode('pc81')#host pc8.1
	pc82 = self.addNode('pc82')#host pc8.2
	pc91 = self.addNode('pc91')#host pc9.1
	pc92 = self.addNode('pc92')#host pc9.2

	#Criacao dos switchs
	sL1 = self.addSwitch('sL1')#switch LAN1
	sL2 = self.addSwitch('sL2')#switch LAN2
	sL3 = self.addSwitch('sL3')#switch LAN3
	sL8 = self.addSwitch('sL8')#switch LAN8
	sL9 = self.addSwitch('sL9')#switch LAN9

	#Criacao dos roteadores A e B
	r1 = self.addSwitch('r1',type='Router')#roteador rA
	r2 = self.addSwitch('r2',type='Router')#roteador rB
	
	#Criacao dos links
	self.addLink(pc11,sL1)
	self.addLink(pc12,sL1)
	self.addLink(pc21,sL2)
	self.addLink(pc22,sL2)
	self.addLink(pc31,sL3)
	self.addLink(pc32,sL3)
	self.addLink(pc81,sL8)
	self.addLink(pc82,sL8)
	self.addLink(pc91,sL9)
	self.addLink(pc92,sL9)
	self.addLink(sL1,r1)
	self.addLink(sL2,r1)
	self.addLink(sL3,r1)
	self.addLink(sL8,r2)
	self.addLink(sL9,r2)
	self.addLink(r1,r2)

	return

def getIP(host):
	#IP de host PC
	if('pc' in host):
		ip = '192.168.'
		ip = ip + host[2] + '.' + host[3] + '/24'
	return ip

def getGateway(host):
	#Gateway de Host PC
	if('pc' in host):
		ip = '192.168.' + host[2] + '.254/24'

	return ip

def main():
    os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")	

    net = Mininet(topo=Topologia())
    net.start()

    #Seta roteador rA e rB
    for router in net.switches:
	if(router.name=='r1' or router.name=='r2'):
        	router.cmd("sysctl -w net.ipv4.ip_forward=1")
        	router.waitOutput()

    #Configura interfaces dos hosts
    for host in net.hosts:
	print("ifconfig %s-eth0 %s" % (host.name, getIP(host.name)))
	host.cmd("ifconfig %s-eth0 %s" % (host.name, getIP(host.name)))
	host.cmd("route add default gw %s" % getGateway(host.name))

    CLI(net)
    net.stop()
    #os.system("killall -9 zebra bgpd")

if __name__ == "__main__":
    main()
