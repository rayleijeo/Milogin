#!/usr/bin/python
#encoding:utf-8
import re 
import json 
import httplib2
import urllib 

#用户名
username='xxx@qq.com'
#密码
password='xxx'
def gethtmlresult(url,methed,headers,body=''):
    http = httplib2.Http() 
    if methed=='POST':
        response,content= http.request(url,methed,headers=headers,body=body);
    else:
        response,content= http.request(url,methed,headers=headers);
        
    if response.status==200:
        print response['set-cookie']
        return content
    elif response.status==302:
       return response; 
    else:
        return response.status
        
    
http = httplib2.Http() 
#第一步  获取 预订页面url
yuyueurl="http://order.mi.com/user/order"
Referer=yuyueurl;
Host=yuyueurl[7:yuyueurl.find('/',7)]
headers={
         'Content-type':'application/x-www-form-urlencoded',
         'Accept':'*/*',
         'Accept-Encoding':
         'gzip,deflate,sdch',
         'Accept-Language':
         'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
         'Connection':'keep-alive',
         'Host':Host} 
content= gethtmlresult(yuyueurl,'GET',headers=headers)
sign=re.findall('var sign = encodeURIComponent\(\"([\s\S]*?)\"\);',content)[0]
qs=re.findall('var qs = encodeURIComponent\(\"([\s\S]*?)\"\);',content)[0]
callback=re.findall('var callback = encodeURIComponent\(\"([\s\S]*?)\"\);',content)[0]
sid=re.findall('var sid = encodeURIComponent\(\"([\s\S]*?)\"\);',content)[0]

#获取sign 打印 
print "token:",sign
#登录url
url = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
body={'user':username,'pwd':password,'_json':'true','sid':sid,'_sign':sign,'callback':callback,'qs':qs}
content =gethtmlresult(url,'POST',headers,urllib.urlencode(body))
utf8content=content.decode("utf-8")
loginresult=json.loads(utf8content[11:])
location=loginresult['location']
yuyueurl=location
print "获取认证链接成功:",location  
headers['Host']=yuyueurl[7:yuyueurl.find('/',10)]
headers['Accept']='text/html, application/xhtml+xml, */*' 
response =gethtmlresult(yuyueurl,'POST',headers)
if response.status==302:
    yuyueurl=response["location"] 
getcookie=response['set-cookie']
pathinfo = re.compile("path=/; domain=(.*?),")
getcookie=pathinfo.sub('',getcookie)
headers['Cookie']=getcookie
content =gethtmlresult(yuyueurl,'GET',headers)
print getcookie 
'''
Referer=yuyueurl 
yuyueurl=urllib.unquote(yuyueurl[yuyueurl.find('=')+1:len(yuyueurl)]);
headers['Cookie']=response['set-cookie']
headers['Accept']='text/html, application/xhtml+xml, */*'
headers['Host']=yuyueurl[8:yuyueurl.find('/',10)]
ffff , fffccc =http.request(yuyueurl,'POST',headers=headers)
print headers
print fffccc.decode("utf-8")
#登录成功后
#print loginresult['desc'],utf8content
''''''
sucresponse , succontent =http.request(location,'GET',headers=headers)
print sucresponse.status,sucresponse['set-cookie']
allcookie=response['set-cookie']+sucresponse['set-cookie'] 
getcookie=re.findall('passToken=([\s\S]*?); Dom',allcookie)
print 'serviceToken='+getcookie[0]

headers={'Cookie':'serviceToken='+getcookie[0],
'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
'Content-type':'application/x-www-form-urlencoded',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip,deflate,sdch',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Host':'order.mi.com',
'DNT':'1',
'Referer':'http://a.hd.mi.com/product/waiting/a/27'} 

newurl = 'http://a.hd.mi.com/product/check/a/27'
ffff , fffccc =http.request(newurl,'POST',headers=headers)
print ffff.status,ffff["location"]
#!response, content = http.request(url, 'GET', headers=headers)'''
