# -*- coding: utf-8 -*-

import sys
import os
import socket

class Whois(object):
	def __init__(self, domain):
		self.domain = domain
		self.tld = self.domain.split(".")[-1]

		self.whoisServers = {}
		f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "whois-servers.conf"), "r")
		exec("self.whoisServers = %s"%(f.read()))

	def chooseServer(self):
		if self.whoisServers.has_key(self.tld):
			return self.whoisServers[self.tld]
		else:
			return self.tld + ".whois-servers.net"

	def run(self, redirect=True):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((self.whoisServer, 43))
		except:
			print "ERROR Could not connect to whois server %s"%(self.whoisServer)
			
		s.send(self.domain + "\r\n")
		
		result = ""

		while True:
			buffer = s.recv(512)

			if not buffer: break 

			result += buffer

		return result 

