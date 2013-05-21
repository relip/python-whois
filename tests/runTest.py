import os 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir) 

from whois import whois
from whois import parser 

print dir(whois)
domain = "example.com"
w = whois(domain, True)
t = w.query(False)
p = parser.Parser(domain, t[1], t[0], True)
print p.parse()
