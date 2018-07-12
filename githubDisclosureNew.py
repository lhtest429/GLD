#coding:utf-8
import requests
import re
import time
import socket
import smtplib  
import urllib
import ssl
from urllib import unquote
from urllib import quote
import urllib2
import json
import string
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage  
from email.header import Header  
import md5

def Mysend_mail(mail_list,sub,content):
    mailto_list=mail_list 
    mail_host=Mail_host  #设置服务器
    mail_user=Mail_user    #用户名
    mail_pass=Mail_pass   #口令 
    mail_postfix=Mail_postfix  #发件箱的后缀
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">" 
    msg = MIMEText(content,_subtype='html',_charset='UTF-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    #msg['To'] = ";".join(mailto_list)  
    for jj in range(0,len(mailto_list)):
        try:  
            server = smtplib.SMTP()  
            server.connect(mail_host)  
            server.login(mail_user,mail_pass)  
            server.sendmail(me, mailto_list[jj], msg.as_string())  
            server.close()
        except Exception, e:  
            print str(e)  
    return True

def loopAccessKey():
	global globalCount
	globalCount = globalCount + 1
	access_token = access_tokenList[globalCount%5]
	return access_token

def get_key(data, pattern):
	regex = re.compile(pattern, re.I)
	result = regex.findall(data)
	return result
def get_github(keywords, page):
	time.sleep(timesleep)
	access_token = loopAccessKey()
	url = 'https://api.github.com/search/code?page='+str(page)+'&per_page=100order=desc&q='+keywords+'&sort=indexed&access_token='+access_token
	url = quote(url,safe=string.printable)
	print url
	try:
		req = urllib2.Request(url)
		req.add_header("User-Agent",UA)
		context = ssl._create_unverified_context()
		resp = urllib2.urlopen(req,context=context,timeout=2000)
		data = unquote(resp.read())
		return data
	except Exception as e:
		print 'error:'+url
		time.sleep(2.5)
		return """{"total_count": 0,  "incomplete_results": false,  "items": [  ]}"""
def getContent(url):
	access_token = loopAccessKey()
	url = url.replace(" ",'%20')+'&access_token='+access_token
	try:
		url = quote(url,safe=string.printable)
		req = urllib2.Request(url)
		req.add_header("User-Agent",UA)
		context = ssl._create_unverified_context()
		resp = urllib2.urlopen(req,context=context,timeout=2000)
		data = unquote(resp.read())
		jsonData = json.loads(data)
		download_url = jsonData['download_url'].encode('utf-8')
		getRealContent(download_url)
	except Exception as e:
		print 'error:'+url
		time.sleep(2.5)
		pass

def getRealContent(download_url):
	download_url = download_url.replace(" ",'%20')
	access_token = loopAccessKey()
	download_url = download_url+'?access_token='+access_token
	try:
		download_url = quote(download_url,safe=string.printable)
		req = urllib2.Request(download_url)
		req.add_header("User-Agent",UA)
		context = ssl._create_unverified_context()
		resp = urllib2.urlopen(req,context=context,timeout=2000)
		data = unquote(resp.read())
		pattern = globalPattern
		result = get_key(data,pattern)
		finalList.extend(result)

	except Exception as e:
		print 'error:'+download_url
		time.sleep(2.5)
		pass
def getRencentTime(url):
	url = url.replace(" ",'%20')
	access_token = loopAccessKey()
	url = url+'?access_token='+access_token
	try:
		url = quote(url,safe=string.printable)
		req = urllib2.Request(url)
		req.add_header("User-Agent",UA)
		context = ssl._create_unverified_context()
		resp = urllib2.urlopen(req,context=context,timeout=2000)
		data = unquote(resp.read())
		updated_at = json.loads(data)['updated_at']
		return updated_at
	except Exception as e:
		print 'error:'+url
		time.sleep(2.5)
		return ''
def get_total_count(keywords):
	time.sleep(timesleep)
	access_token = loopAccessKey()
	url = 'https://api.github.com/search/code?page=1&per_page=100order=desc&q='+keywords+'&sort=indexed&access_token='+access_token
	url = quote(url,safe=string.printable)
	try:
		req = urllib2.Request(url)
		req.add_header("User-Agent",UA)
		context = ssl._create_unverified_context()
		resp = urllib2.urlopen(req,context=context,timeout=2000)
		data = unquote(resp.read())
		jsonContent = json.loads(data)
		total_count = jsonContent['total_count']
		return total_count
	except Exception as e:
		print 'error:'+url
		time.sleep(2.5)
		return 0

def specifySearch(key):
	MaxPage = maxpageFor_Compare
	total_count = get_total_count(key)
	if total_count>0:
		for page in range(1,MaxPage):
			print page
			content = get_github(key,page)
			jsonContent = json.loads(content)
			items = jsonContent['items']
			if len(items) == 0:
				break
			if page == 1 and len(items)>0:
				rencentURL = items[0]['repository']['owner']['url']
				html_url = items[0]['html_url']
				updated_at = getRencentTime(rencentURL)
				fileread = open('result/gitresult.txt','r')
				contentRead = fileread.readlines()
				fileread.close()
				myflag = 0
				for line in contentRead:
					line = line.strip()
					array = line.split('	')
					if key == array[0]:
						myflag = 1
						historyList.append(key+'	'+updated_at)
						if array[1] != updated_at:
							print key+' not the same,the new is'+updated_at
							try:
								Mysend_mail(Mailto_list, 'new gitHub Disclosure is found!','new github leak '+ key +' not the same,the new is'+updated_at+'\n'+html_url)
							except Exception as e:
								Mysend_mail(Mailto_list, 'new gitHub Disclosure is found!','new github leak '+ key +' not the same,the new is'+updated_at+'\n')
							break
				
				if myflag == 0:
					historyList.append(key+'	'+updated_at)
					print key+' is first apperence'+updated_at
					try:
						Mysend_mail(Mailto_list, 'new gitHub Disclosure is found!','new github leak '+ key+' is first apperence'+updated_at+'\n'+html_url)
					except Exception as e:
						Mysend_mail(Mailto_list, 'new gitHub Disclosure is found!','new github leak '+ key+' is first apperence'+updated_at+'\n')
				print updated_at
			for i in range(0,len(items)):
				url = items[i]['url'].strip().encode('utf-8')
				#print url
				getContent(url.strip())
def getAllSearch(key):
	MaxPage = maxpageFor_Email
	total_count = get_total_count(key)
	if total_count>0:
		for page in range(1,MaxPage):
			print page
			content = get_github(key,page)
			jsonContent = json.loads(content)
			items = jsonContent['items']
			if len(items) == 0:
				break
			for i in range(0,len(items)):
				url = items[i]['url'].strip().encode('utf-8')
				getContent(url.strip())

while(True):
	globalPattern = ''
	Mail_host = "" 
	Mail_user="" 
	Mail_pass=""
	Mail_postfix=""
	maxpageFor_Compare = 3
	maxpageFor_Email = 4
	globalUA = ''	

	configlines = open('conf/config.txt','r').readlines()
	for config in configlines:
		array = config.split('=')
		key = array[0]
		value = array[1]
		if key.find('globalPattern')>-1:
			globalPattern = value.strip()
		if key.find('Mail_host')>-1:
			Mail_host = value.strip()
		if key.find('Mail_user')>-1:
			Mail_user = value.strip()
		if key.find('Mail_pass')>-1:
			Mail_pass = value.strip()
		if key.find('Mail_postfix')>-1:
			Mail_postfix = value.strip()
		if key.find('maxpageFor_Compare')>-1:
			maxpageFor_Compare = int(value.strip())
		if key.find('maxpageFor_Email')>-1:
			maxpageFor_Email = int(value.strip())
		if key.find('globalUA')>-1:
			globalUA = value.strip()	
	access_tokenList = open('conf/access_token.txt','r').readlines()
	Mailto_list = open('conf/receiveEmail.txt','r').readlines()

	starttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print 'scan start at 'starttime
	UA = globalUA
	wrongEmailList = open('conf/WrongList.txt','r').readlines()
	WhiteList = open('conf/WhiteList.txt','r').readlines()
	global globalCount
	globalCount = 0
	timesleep = float(5000/3600 + 1 + 1)/float(len(access_tokenList))
	historyList = list()
	finalList = list()
	###################ScanType1################################
	CompareKeyWord = open('keywords/CompareKeyWord.txt','r').readlines()
	for keyword in CompareKeyWord:
		specifySearch(keyword)
	if historyList is not None:
		filewrite = open('result/gitresult.txt','w')
		for line in historyList:
			filewrite.write(line.strip()+'\n')
		filewrite.close()	
	###################ScanType2################################
	keywordList = open('keywords/keyWordList.txt','r').readlines()
	for keyword in keywordList:
		getAllSearch(keyword.strip())
		lastFinalList = list()
		strFinal = ''

	for line in finalList:
		if line[0].strip() not in wrongEmailList and line[0].strip() not in WhiteList:
			lastFinalList.append(line[0].strip())
			strFinal = strFinal+line[0].strip()+'\n'	

	lastFinalList = list(set(lastFinalList))
	print lastFinalList
	stoptime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print 'scan stop at 'stoptime
	Mysend_mail(Mailto_list, 'new gitHub Disclosure is found!',str(lastFinalList)+'\n'+'is found')

