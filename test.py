
import re
import string
import sys
import os
import urllib
import urllib3,certifi
from bs4 import BeautifulSoup
import lxml.etree
import lxml.html as x



url = 'http://detail.1688.com/offer/42769715160.html'
headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)'}

pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

r = pool.request("GET",url,headers=headers)

html = r.data
##soup = BeautifulSoup(html,"lxml")
##
##print(soup.prettify())
##f=open('test.html','rb')
##c=f.read()
doc=x.document_fromstring(html)
alist=doc.xpath('//li[@data-page-name="contactinfo"]/a')
url=alist[0].attrib['href']

r = pool.request("GET",url,headers=headers)
doc=x.document_fromstring(r.data)
contactname=doc.xpath('//div[@class="contact-info"]/dl/dd/a')[0].text
print(contactname)
contactdesc=doc.xpath('//div[@class="contcat-desc"]/dl/dd')
for desc in contactdesc:
    print(desc.text)


