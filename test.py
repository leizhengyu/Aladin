
import re
import string
import sys
import os
import urllib
import urllib3
from bs4 import BeautifulSoup
import lxml.etree
import lxml.html as x



url = 'http://www.baidu.com'

pool = urllib3.PoolManager()

r = pool.request("GET",url)

html = r.data.decode()

##soup = BeautifulSoup(html,"lxml")
##
##print(soup.prettify())
f=open('test.html','rb')
c=f.read()
doc=x.document_fromstring(c)
body=doc.xpath('//*[@id="sm-maindata"]/div')[0]
alist=body.xpath('//div[@class="imgofferresult-mainBlock"]/div/a')

for a in alist:
    tree=lxml.etree.ElementTree(a)
    print(tree.getpath(a))
