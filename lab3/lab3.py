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
        pc11 = self.addNode('pc11',ip='172.16.10.1')#host pc1.1
	pc12 = self.addNode('pc12',ip='172.16.10.2')#host pc1.2
	pc21 = self.addNode('pc21',ip='172.16.20.1')#host pc2.1
	pc22 = self.addNode('pc22',ip='172.16.20.2')#host pc2.2
	pc31 = self.addNode('pc31',ip='172.16.30.1')#host pc3.1
	pc32 = self.addNode('pc32',ip='172.16.30.2')#host pc3.2
	pc81 = self.addNode('pc81',ip='172.16.40.1')#host pc8.1
	pc82 = self.addNode('pc82',ip='172.16.40.2')#host pc8.2
	pc91 = self.addNode('pc91',ip='172.16.50.1')#host pc9.1
	pc92 = self.addNode('pc92',ip='172.16.50.2')#host pc9.2
	pc101 = self.addNode('pc101',ip='172.16.60.1')#host pc10.1
	pc102 = self.addNode('pc102',ip='172.16.60.2')#host pc10.2

	#Criacao dos switchs
	sL10 = self.addSwitch('sL10')#switch LAN10
	sL20 = self.addSwitch('sL20')#switch LAN20
	sL30 = self.addSwitch('sL30')#switch LAN30
	sL40 = self.addSwitch('sL40')#switch LAN40
	sL50 = self.addSwitch('sL50')#switch LAN50
	sL60 = self.addSwitch('sL60')#switch LAN60

	#Criacao dos roteadores A e B
	r1 = self.addSwitch('r1',type='Router')#roteador SP
	r2 = self.addSwitch('r2',type='Router')#roteador RJ
	r3 = self.addSwitch('r3',type='Router')#roteador BH

	#Criacao dos links
	self.addLink(pc11,sL10)
	self.addLink(pc12,sL10)
	self.addLink(pc21,sL20)
	self.addLink(pc22,sL20)
	self.addLink(pc31,sL30)
	self.addLink(pc32,sL30)
	self.addLink(pc81,sL40)
	self.addLink(pc82,sL40)
	self.addLink(pc91,sL50)
	self.addLink(pc92,sL50)
	self.addLink(pc101,sL60)
	self.addLink(pc102,sL60)
	self.addLink(sL10,r2)
	self.addLink(sL20,r2)
	self.addLink(sL30,r1)
	self.addLink(sL40,r1)
	self.addLink(sL50,r3)
	self.addLink(sL60,r3)
	self.addLink(r2,r1)
	self.addLink(r1,r3)
	

	return


def main():
    os.system("rm -f /tmp/r*.log /tmp/r*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")	
    os.system("killall -9 zebra > /dev/null 2>&1")
    os.system('pgrep -f webserver.py | xargs kill -9')

    net = Mininet(topo=Topologia())
    net.start()

	

    #Seta roteador rA e rB
    for router in net.switches:
	if(router.name=='r1' or router.name=='r2' or router.name=='r3'):
        	router.cmd("sysctl -w net.ipv4.ip_forward=1")
        	router.waitOutput()

    #Configura interface do roteador sp e bh e rj com zebra e bgpd
    for router in net.switches:
        if(router.name=='r2' or router.name=='r1' or router.name=='r3'):
       		router.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
        	router.waitOutput()
		router.cmd("/usr/lib/quagga/bgpd -f conf/bgpd-%s.conf -d -i /tmp/bgp-%s.pid > logs/%s-bgpd-stdout 2>&1" % (router.name, router.name, router.name), shell=True)
        	router.waitOutput()
		
  
    CLI(net)
    net.stop() 
    os.system("killall -9 zebra bgpd")
   

if __name__ == "__main__":
    main()
