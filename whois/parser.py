# -*- coding: utf-8 -*-

# ______  ______   ______   ______   ______   ______    
#/\  == \/\  __ \ /\  == \ /\  ___\ /\  ___\ /\  == \   
#\ \  _-/\ \  __ \\ \  __< \ \___  \\ \  __\ \ \  __<   
# \ \_\   \ \_\ \_\\ \_\ \_\\/\_____\\ \_____\\ \_\ \_\ 
#  \/_/    \/_/\/_/ \/_/ /_/ \/_____/ \/_____/ \/_/ /_/ 

import error
import re 
import sys
import os 

import logging 

class Parser(object):
	def __init__(self, domain, text, whoisServer=None, debug=False):
		if debug:
			logging.basicConfig(level=logging.DEBUG)
			logging.debug("__init__: DEBUG is set to True")

		self.domain = domain
		self.text = text
		self.whoisServer = whoisServer and whoisServer or "default"

		self.tld = self.domain.split(".")[-1]

		self.currPath = os.path.dirname(os.path.realpath(__file__))
		self.tldPath = os.path.join(self.currPath, "tlds")

		logging.debug("__init__: Setting initial variables...\nself.domain: %s\nself.text = %s\nself.whoisServer = %s\nself.tld = %s\nself.currPath = %s\nself.tldPath = %s"
			%(self.domain, self.text, self.whoisServer, self.tld, self.currPath, self.tldPath)) 

		self.parseDefaultConf = {} 
		logging.debug("__init__: Loading default tld configuration file") 
		execfile(os.path.join(self.tldPath, "default"), {}, self.parseDefaultConf)
		self.parseDefaultConf = self.parseDefaultConf.get("parse")

		self.parseConf = {}

		try:
			execfile(os.path.join(self.tldPath, self.tld), {}, self.parseConf)
		
			self.parseConf = self.parseConf.get("parse")

			# NO "parse" in the tld config AND YES regex for specified server in default conf

			if not self.parseConf and whoisServer not in self.parseDefaultConf:
				self.parseConf = self.parseDefaultConf.get("default")

			# END
			# 
			# NO "parse" in the tld config 

			elif not self.parseConf:
				self.parseConf = self.parseDefaultConf.get(whoisServer) 

			# END
			#
			# YES "parse" in the tld config AND YES regex for specified server 

			elif self.whoisServer in self.parseConf:
				self.parseConf = self.parseConf.get(self.whoisServer)

			# END
			#
			# YES "parse" in the tld config AND YES "default" regex in the tld config AND
			# NO regex for specified server

			elif "default" in self.parseConf:
				self.parseConf = self.parseConf.get("default")

			# END
			#
			# YES "parse" in the tld config AND NO "default" regex in the tld config
			# MAYBE empty file? 

			else: 
				self.parseConf = self.parseDefaultConf.get("default")

			# END

			# Check for LoadConf 
			_parseConf = self.parseConf
			self.parseConf = {} 

			if "LoadConf" in _parseConf:
				logging.debug("__init__: LoadConf found in parser config")
				try:
					# <tld>/<whois server>
					# e.g. org/whois.publicinternetregistry.net
					lc = _parseConf["LoadConf"].split("/", 1)
			
					lcTLD = lc[0]
					lcWS = lc[1]
						
					lcConf = {}

					logging.debug("__init__: Loading configuration file of tld name %s"%(lcTLD))

					execfile("tlds/%s"%(lcTLD), {}, lcConf)
					lcConf = lcConf.get("parse")

					self.parseConf.update(lcConf.get(lcWS))

				except: 
					pass

			self.parseConf.update(_parseConf)

		except:
			self.parseConf = self.parseDefaultConf.get("default")


		logging.debug("__init__: self.parseConf = %s"%(self.parseConf))


	def run(self):
		result = {}
		for key in self.parseConf:
			matches = re.findall(self.parseConf[key], self.text, re.MULTILINE)
			if matches:
				logging.debug("run: regex matches found for key %s. %s"%(key, matches))
				result.update({key: map(lambda x: x.strip(), matches)})

			else:
				logging.debug("run: No match for %s"%(key))

		print result
