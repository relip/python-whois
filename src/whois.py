# -*- coding: utf-8 -*-

import sys
import os
import socket
import re

class Whois(object):
	def __init__(self, domain):
		self.domain = domain
		self.tld = self.domain.split(".")[-1]

		self.currPath = os.path.dirname(os.path.realpath(__file__))
		self.tldPath = os.path.join(self.currPath, "tlds")
		self.tldList = os.listdir(self.tldPath)

		self.settings = {}

		if self.tld in self.tldList:
			self.settings = {}
			execfile(os.path.join(self.tldPath, self.tld), {}, self.settings)

	def chooseServer(self):
		if "server" in self.settings:
			return self.settings["server"]["host"]
		else:
			return self.tld + ".whois-servers.net"

	def query(self, whoisServer):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			s.connect((whoisServer, 43))
		except:
			# FIXME: Create a exception class for this 
			print "ERROR Could not connect to whois server %s"%(whoisServer)
			return False 
			
		s.send(self.domain + "\r\n")
		
		result = ""

		while True:
			buffer = s.recv(512)

			if not buffer: 
				break 

			result += buffer

		return result 

	def run(self, redirect=True):
		result = self.query(self.chooseServer())

		if redirect:
			redirection = re.findall(self.settings["server"]["redirect"], result, re.MULTILINE)

			while redirection and len(redirection) >= 1:
				result = self.query(redirection[0])
				redirection = re.findall(self.settings["server"]["redirect"], result)


		return result

		
