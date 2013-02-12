# -*- coding: utf-8 -*-

# __     __   __  __   ______   __   ______    
#/\ \  _ \ \ /\ \_\ \ /\  __ \ /\ \ /\  ___\   
#\ \ \/ ".\ \\ \  __ \\ \ \/\ \\ \ \\ \___  \  
# \ \__/".~\_\\ \_\ \_\\ \_____\\ \_\\/\_____\ 
#  \/_/   \/_/ \/_/\/_/ \/_____/ \/_/ \/_____/ 

import sys
import os
import socket
import re

import error

class Whois(object):
	def __init__(self, domain):
		self.domain = domain
		self.tld = self.domain.split(".")[-1]

		self.currPath = os.path.dirname(os.path.realpath(__file__))
		self.tldPath = os.path.join(self.currPath, "tlds")
		self.tldList = os.listdir(self.tldPath)

		self.settings = {}

		if self.tld in self.tldList:
			_settings = {}
			execfile(os.path.join(self.tldPath, self.tld), {}, _settings)

			if "server" in _settings:
				self.settings.update(_settings["server"])

	def chooseServer(self):
		if "host" in self.settings:
			return self.settings["host"]
		else:
			return self.tld + ".whois-servers.net"

	def sendQuery(self, whoisServer):
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

		return result.replace("\r\n", "\n")

	def query(self, redirect=True):
		whoisServer = self.chooseServer()
		result = self.sendQuery(whoisServer)

		if redirect and "redirect" in self.settings:
			redirection = re.findall(self.settings["redirect"], result, re.MULTILINE)

			while redirection and len(redirection) >= 1:
				whoisServer = redirection[0]
				result = self.sendQuery(whoisServer)
				redirection = re.findall(self.settings["redirect"], result)


		return whoisServer, result
