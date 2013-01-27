# -*- coding: utf-8 -*-

import sys
import os
import socket

class Whois(object):
	def __init__(self, domain):
		self.domain = domain
		self.tld = self.domain.split(".")[-1]

		self.currPath = os.path.dirname(os.path.realpath(__file__))
		self.tldPath = os.path.join(self.currPath, "tlds")
		self.tldList = os.listdir(self.tldPath)

	def chooseServer(self):
		if self.tld in self.tldList:
			settings = {}
			execfile(os.path.join(self.tldPath, self.tld), {}, settings)
			if "server" in settings:
				return settings["server"]
			else:
				return self.tld + ".whois-servers.net"

		else:
			return self.tld + ".whois-servers.net" 


	def run(self, redirect=True):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.whoisServer = self.chooseServer()
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

