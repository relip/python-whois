import os 

whoisServers = {} 
execfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "whois-servers.conf"), {}, whoisServers)
print whoisServers
