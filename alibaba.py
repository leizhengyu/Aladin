import urllibimport urllib3,certifiimport jsonimport refrom lxml import etree as ETimport lxml.htmlimport stringdef get_infolist(httpurl,keywords):    url =httpurl + "&keywords=" + urllib.parse.quote(keywords.encode(charset))    for i in range(1,100):        url +="&beginPage=%d"% i        rtn=get_info(url)        if rtn == 1 :            exit()def get_info(url):    rsp = pool.request("GET",url,headers=headers)    srsp = rsp.data.decode(charset)[1:-2]    srsp=srsp.replace("\\'","'")    jsrsp = json.loads(srsp)    htmlsrc = jsrsp["content"]["offerResult"]["html"]    doc = lxml.html.document_fromstring(htmlsrc)    alist=doc.xpath('//a[@class="sm-offer-companyName sw-dpl-offer-companyName "]')    if len(alist) == 0:        print("asdf")        return 1    else :        for a in alist:            href=a.attrib['href']            rx = re.compile(r'http://\w+\.1688\.com')            url=rx.findall(href)[0] + '/page/contactinfo.html'            print(url)            data=get_seller(url)            print(data)        return 0def get_seller(url):    rsp=pool.request("GET",url,headers=headers)    doc=lxml.html.document_fromstring(rsp.data)    companyName = doc.xpath('//div[@class="contact-info"]/h4/text()')[0]    contactname = doc.xpath('//div[@class="contact-info"]/dl/dd/a/text()')[0]    contactdesc = doc.xpath('//div[@class="contcat-desc"]/dl/dd/text() | //div[@class="contcat-desc"]/dl/dt/text()')    info = "#".join(contactdesc)    mc = re.search(r'电      话：#(.*?)\s*#',info,re.MULTILINE|re.UNICODE)    tel = "" if mc == None else mc.group(1).strip()    mc = re.search(r'移动电话：#(.*?)\s*#',info,re.MULTILINE|re.UNICODE)    mobile = "" if mc == None else mc.group(1).strip()    mc = re.search(r'传      真：#(.*?)\s*#',info,re.MULTILINE|re.UNICODE)    fax = "" if mc == None else mc.group(1).strip()    mc = re.search(r'地      址：#(.*?)\s*#',info,re.MULTILINE|re.UNICODE)    addr = "" if mc == None else mc.group(1).strip()    mc = re.search(r'邮      编：#(.*?)\s*#',info,re.MULTILINE|re.UNICODE)    zipcode = "" if mc == None else mc.group(1).strip()    print(tel)    website=doc.xpath('//div[@class="contcat-desc"]/dl/dd/div/a')    wbs=[]    for wb in website:        wbs.append(wb.attrib['href'].strip())    data = {"name": contactname,            "tel" : tel,            "mobile": mobile,            "fax": fax,            "addr": addr,            "zipcode": zipcode,            "website": wbs            }    return data# 1. start and connect to serverjs=json.loads('{"KEYS":"",         \                "BASE":{"http": "http://s.1688.com","Headers":"content=IE9","path":"/selloffer/offer_search.htm?keywords="}, \                "PATH":[{"xpath":"<a><b><c><d>","action":"open/parse"},    \                        {"xpath":"asdf","action":"parse"},                 \                        {"xpath":"asdf","action":"parse"}]}')# 2. create thead and send messagekeywords = js['KEYS']baseaddr = js['BASE']xpaths   = js['PATH']pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())rsp = pool.request("GET",baseaddr['http']);ct=rsp.headers['Content-Type']regex = re.compile(r'.*; charset=(\w+)')match=regex.match(ct)if match :    charset=match.group(1)else:    charset='utf-8'headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)','Accept':'text/html;q=0.9,*/*;q=0.8','Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding':'GBK,utf-8;q=0.7,*;q=0.3','Connection':'close','Referer':'http://s.1688.com'}url = "https://s.1688.com/selloffer/rpc_async_render.jsonp?rpcflag=new&_serviceId_=marketOfferResultViewService&startIndex=0&_template_=controls%2Fnew_template%2Fproducts%2Fmarketoffersearch%2Fofferresult%2Fpkg-a%2Fviews%2Fofferresult.vm&enableAsync=true&button_click=top&asyncCount=60&n=y&offset=9&async=true&token=2321131414"get_infolist(url,keywords)