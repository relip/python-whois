python-whois
============

The whois library, which is developed in Python language, retrieves domain information from the server.

Quick start
-----------

1. Install the library

	python setup.py install

2. Run Python interpreter
	
	python

3. To get whois data of example.com

	import whois
	whoisData = whois.whois("example.com").query()

whois.whois will return tuple type, which contains whois server address and the whois data. 

To parse whois data, 

	>>> result = whois.parser("example.com", whoisData[1])

Some whois servers of top level domains (like .com and .net) send redirect command in order to let clients to get more information, like address and phone number, from whois server of domain reseller. However, all whois servers have all different data format. So if you want parse the whois data more accurately, I recommend to set "redirect" parameter to `False` when querying, or if you want detailed information, please add data format of the whois server to tld config file and make a pull request.

Config file structure
-----------
