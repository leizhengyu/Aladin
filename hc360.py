import urllib
import urllib3,certifi
import json
import re
import lxml.etree
import lxml.html
import string
from socket import *

def get_infolist(httpurl,keywords):
    url = httpurl + "&w=" + urllib.parse.quote(keywords.encode(charset))

    i =0
    while 1 :
        i += 1
        for af in [0,3]:
            ee = "" if i == 1 else "&ee=%d"%i
            page = url + ee
            page += "" if af ==0 else "&af=%d"% af
            print(page)
            rtn = get_info(page)
            if rtn == 1 :
                exit()

def get_info(url):

    rsp = pool.request("GET",url,headers=headers)

    doc = lxml.html.document_fromstring(rsp.data)

    alist=doc.xpath('//dd[@class="til"]/h3/a[@data-exposurelog]')

    if len(alist) == 0:
        return 1
    else :
        for a in alist:
            href=a.attrib['href']
            # rx = re.compile(r'http://\w+\.1688\.com')
            url = href  + '/pubinfo/businesscard.html'
            print(url)
            data = get_seller(url)
            if data != None :
                jsdata = json.dumps(data)
                client.send(jsdata.encode("utf-8"))
                print(data)
        return 0


def get_seller(url):
    try:
        rsp=pool.request("GET",url,headers=headers)
        if rsp.status == 404 :
            return
        doc=lxml.html.document_fromstring(rsp.data)
        companyName = doc.xpath('head/title/text()')
        name = doc.xpath('//a[@class="name"]/text()')[0]
        info = doc.xpath('//span[@class="px1216"]/text()')
        strinfo = "#".join(info) + "#"
        mc = re.search(r"地址：(.*?)\s*#",strinfo,re.MULTILINE)
        addr = "" if mc == None else mc.group(1)

        mc = re.search(r'邮编：(.*?)\s*#',strinfo,re.MULTILINE)
        zipcode = "" if mc == None else mc.group(1)
        mctel = re.search(r'电话：(.*?)\s*#',strinfo,re.MULTILINE)
        tel = "" if mc == None else mc.group(1)
        mcmobile = re.search(r'手机：(.*?)\s*#',strinfo,re.MULTILINE)
        mobile = "" if mc == None else mc.group(1)
        mcfax = re.search(r'传真：(.*?)\s*#',strinfo,re.MULTILINE)
        fax = "" if mc == None else mc.group(1)

        website=doc.xpath('//span[@class="px1216"]/a')
        wbs=[]
        for wb in website:
            wbs.append(wb.attrib['href'].strip())

        data = {"name": name,
                "tel" : tel,
                "mobile": mobile,
                "fax": fax,
                "addr": addr,
                "zipcode":zipcode,
                "website":wbs
                }
        return data
    except:
        return




# 1. start and connect to server


js=json.loads('{"KEYS":"净化器",         \
                "BASE":{"http": "http://s.hc360.com","Headers":"content=IE9","path":"/selloffer/offer_search.htm?keywords="}, \
                "PATH":[{"xpath":"<a><b><c><d>","action":"open/parse"},    \
                        {"xpath":"asdf","action":"parse"},                 \
                        {"xpath":"asdf","action":"parse"}]}')
# 2. create thead and send message

keywords = js['KEYS']
baseaddr = js['BASE']
xpaths   = js['PATH']

pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

rsp = pool.request("GET",baseaddr['http']);
ct=rsp.headers['Content-Type']
regex = re.compile(r'.*; charset=(\w+)')
match=regex.match(ct)
if match :
    charset=match.group(1)
else:
    charset='utf-8'

headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'GBK,utf-8;q=0.7,*;q=0.3',
'Connection':'close',
'Referer':'http://s.hc360.com'
}


url = "http://s.hc360.com/?mc=enterprise"

host = '127.0.0.1'
port = 456
bufsize = 1024
addr = (host,port)
client = socket(AF_INET,SOCK_DGRAM)
client.connect(addr)



get_infolist(url,keywords)

client.close()


