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
import logging

import error

class Whois(object):
	def __init__(self, domain, debug=False):
		if debug: 
			logging.basicConfig(level=logging.DEBUG)
			logging.debug("__init__: DEBUG is set to True")

		self.domain = domain
		self.tld = self.domain.split(".")[-1]

		self.currPath = os.path.dirname(os.path.realpath(__file__))
		self.tldPath = os.path.join(self.currPath, "tlds")
		self.tldList = os.listdir(self.tldPath)

		logging.debug("__init__: Setting initial variables.. self.currPath = %s / self.tldPath = %s / self.tldList = %s"
			%(self.currPath, self.tldPath, self.tldList))

		self.settings = {}

		if self.tld in self.tldList:
			logging.debug("__init__: Loading tld configuration file...")

			_settings = {}
			execfile(os.path.join(self.tldPath, self.tld), {}, _settings)

			if "server" in _settings:
				logging.debug("__init__: Settings: %s"%(_settings["server"]))
				self.settings.update(_settings["server"])
			else:
				logging.debug("__init__: No server settings found")

	def chooseServer(self):
		if "host" in self.settings:
			logging.debug("chooseServer: Whois server addr: %s"%(self.settings["host"]))
			return self.settings["host"]
		else:
			logging.debug("chooseServer: Whois server addr: %s"%(self.tld + ".whois-servers.net"))
			return self.tld + ".whois-servers.net"

	def sendQuery(self, whoisServer):
		logging.debug("sendQuery: Connecting to whois server")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			s.connect((whoisServer, 43))

		except:
			# FIXME: Create a exception class for this 
			logging.error("sendQuery: Error connecting to whois server %s"%(whoisServer))
			return False 

		try:
			msg = self.settings['format'][whoisServer].replace("%DOMAIN%", self.domain) + "\r\n"

		except:
			msg = self.domain + "\r\n"

		logging.debug("sendQuery: Sending data.. %s"%(msg))

		s.send(msg)
		
		result = ""

		while True:
			buffer = s.recv(512)

			if not buffer: 
				break 

			result += buffer

		finalResult = result.replace("\r\n", "\n")

		logging.debug("sendQuery: result: %s"%(finalResult))

		return finalResult

	def query(self, redirect=True):
		whoisServer = self.chooseServer()
		result = self.sendQuery(whoisServer)

		if redirect and "redirect" in self.settings:
			logging.debug("query: Redirection found. Connecting to given server address")

			redirection = re.findall(self.settings["redirect"], result, re.MULTILINE)

			while redirection and len(redirection) >= 1:
				whoisServer = redirection[0]
				result = self.sendQuery(whoisServer)
				redirection = re.findall(self.settings["redirect"], result)


		return whoisServer, result
