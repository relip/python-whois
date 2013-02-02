# -*- coding: utf-8 -*-

import error
import re 

class Parser(object):
	def __init__(self, domain, text, whoisServer=None):
		self.domain = domain
		self.text = text
		self.whoisServer = whoisServer and whoisServer or "default"

		self.tld = self.domain.split(".")[-1]

		self.parseDefaultConf = {} 
		execfile("tlds/default", {}, self.parseDefaultConf)
		self.parseDefaultConf = self.parseDefaultConf.get("parse")

		self.parseConf = {}

		try:
			execfile("tlds/%s"%(self.tld), {}, self.parseConf)
		
			self.parseConf = self.parseConf.get("parse")

			if not self.parseConf and whoisServer not in self.parseDefaultConf:
				self.parseConf = self.parseDefaultConf.get("default")

			elif not self.parseConf:
				self.parseConf = self.parseDefaultConf.get(whoisServer) 

			elif self.whoisServer in self.parseConf:
				self.parseConf = self.parseConf.get(self.whoisServer)

			elif "default" in self.parseConf:
				self.parseConf = self.parseConf.get("default")

			else: 
				self.parseConf = self.parseDefaultConf.get("default")

			# Check for LoadConf 
			_parseConf = self.parseConf
			self.parseConf = {} 

			if "LoadConf" in _parseConf:
				try:
					# <tld>/<whois server>
					# e.g. org/whois.publicinternetregistry.net
					lc = _parseConf["LoadConf"].split("/", 1)
			
					lcTLD = lc[0]
					lcWS = lc[1]
						
					lcConf = {}
					execfile("tlds/%s"%(lcTLD), {}, lcConf)
					lcConf = lcConf.get("parse")

					self.parseConf.update(lcConf.get(lcWS))

				except: 
					pass

			self.parseConf.update(_parseConf)

		except:
			self.parseConf = self.parseDefaultConf.get("default")

	def run(self):
		result = {}
		for key in self.parseConf:
			matches = re.findall(self.parseConf[key], self.text, re.MULTILINE)
			if matches:
				result.update({key: map(lambda x: x.strip(), matches)})

		print result
