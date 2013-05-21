python-whois
============

The whois library, which is developed in Python language, retrieves domain information and ip allocation information (WiP) from the server.

Quick start
-----------

Install the library.

	python setup.py install

Run Python interpreter.
	
	python

To get whois data of example.com,

	import whois
	whoisData = whois.whois("example.com").query()

whois.whois will return tuple type, which contains whois server address and the whois data. 

To parse whois data, 

	result = whois.Parser("example.com", whoisData[1]).parse()

Some whois servers of top level domains (like .com and .net) send redirect command in order to let clients to get more information, like address and phone number, from whois server of domain reseller. However, all whois servers have all different data format. So if you want parse the whois data more accurately, I recommend to set "redirect" parameter to `False` when querying, or if you want detailed information, please add data format of the whois server to tld config file and make a pull request.

Config file structure
-----------

	server = {
		"host": "net.whois-servers.net",
		"redirect": "\s+Whois Server: (.*)",
	}
	
	parse = {
		"default": {
			"NotFound": "No match for domain",
			"DomainName": "Domain Name:\s+(.+)",
			"Registrar": "Registrar:\s+(.+)",
			"NameServer": "Name Server:\s+(.+)",
			"Status": "Status:\s+(.+)",
			"UpdatedDate": "Updated Date:\s+(.+)",
			"CreationDate": "Creation Date:\s+(.+)",
			"ExpirationDate": "Expiration Date:\s+(.+)",
		},
		"whois.dotname.co.kr":
		{

		},
	}



