#!/usr/bin/env python

# user defined variables
debug = True
urlBase = "http://websta.me/location/7428634"

# Functions
def d(msg):
	if not debug:
		return
	
	print msg

def makeDir(dir):
	if os.path.exists(dir):
		d('Directory "' + dir + '" already exists. Continuing.')
		return True
		
	d('Creating directory "' + dir + '" ...')
	os.makedirs(dir)

	if not os.path.exists(dir):
		d('Directory "' + dir + '" not created.')
		return False

	d('Directory "' + dir + '" created.')
	return True

def writeFile(path,content,append = True):
	if append:
		mode = 'a'
	else:
		mode = 'w'
	
	file = open(path,mode)
	
	if type(content) == type(list()):
		#d('content is of type list. Converting it into a newline separated string before writing to file.')
		content = "\n".join(content) + "\n"
	
	file.write(content)
	file.close()
	
	return True

def getInstagramPics(body):
	'''
	<a href="/p/848877224061586781_657671810" class="mainimg">
	<img src="http://scontent-b.cdninstagram.com/hphotos-xpf1/t51.2885-15/10735151_559130887522169_489118905_a.jpg" width="306" heigh="306">
	</a>
	'''
	
	soup = BeautifulSoup(body)
	anchors = soup.findAll('a', { 'class':'mainimg' })
	
	images = []
	
	for anchor in anchors:
		img = anchor.find('img')
		src = img['src']
		
		d('   ' + src)
		
		images.append(src)
	
	return images

def getNextPageURL(body):
	'''
	<ul class="pager">
	<li><a href="/location/7428634/?npk=836659987415347067"><i class="fa fa-chevron-down"></i> Earlier</a></li>
	</ul>
	'''
	
	soup = BeautifulSoup(body)
	ul = soup.find('ul', { 'class':'pager' })
	
	try:
		anchor = ul.find('a')
	except:
		d('Could not retrieve <ul class="pager">. Aborting.')
		return False
	
	try:
		href = 'http://websta.me' + anchor['href']
	except:
		d('Could not retrieve anchor[href]. Aborting.')
		return False
	
	return href

def getRangeId(url):
	m = re.search('npk=([0-9]+)', url)
	id = m.group(1)
	
	return id

def isList(var):
	return isinstance(var, (list, tuple))

# basic modules
import sys
import os

# http://community.sitepoint.com/t/python-equivil-equivalent-to-phps-explode-function/4520
import string

# https://docs.python.org/2/library/re.html
import re

# http://stackoverflow.com/questions/645312/what-is-the-quickest-way-to-http-get-in-python
import urllib2

# http://docs.python-requests.org/en/latest/
import requests

# http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
from BeautifulSoup import BeautifulSoup

url = urlBase
m = re.search('location/([0-9]+)', url)
id = m.group(1)

dir = './cache/' + id
res = makeDir(dir)

if not res:
	d('Could not create directory "' + dir + '". Aborting')
	exit(1)

pathImageURLs = dir + '/urls.txt'

cont = True

counterPages = 0
counterImages = 0
while cont:
	d('Trying to retrieve URL "' + url + '" ...')
	
	r = requests.get(url)
	body = r.content
	
	counterPages += 1
	
	if counterPages == 1:
		path = dir + '/index.html'
	else:
		path = dir + '/' + getRangeId(url) + '.html'
	
	d('Writing HTTP response to file "' + path + '" ...')
	writeFile(path,body,False)
	
	d('Parsing HTTP response for Instagram image URLs ...')
	images = getInstagramPics(body)
	
	counterImages += len(images)
	
	d('Writing Instagram URLS to "' + pathImageURLs + '" ...')
	writeFile(pathImageURLs,images)
	
	url = getNextPageURL(body)
	
	if url == False:
		d('Could not retrieve any further paging URL. Aborting.')
		break
	
	d('Next URL is "' + url + '"')
	d('')

d('Finished crawling ' + str(counterPages) + ' pages from websta.me, resulting in ' + str(counterImages) +' Instapaper image URLs')

exit(0)