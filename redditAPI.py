Author = "b4dnew"
Version = "0.1"
Platform = "Python"

import json
import urllib2
import urllib

typePrefixes = {"t1_": "Comment",
				"t2_": "Account",
				"t3_": "Link",
				"t4_": "Message",
				"t5_": "Subreddit",
				"t6_": "Award",
				"t8_": "PromoCampaign"
			   }

SiteUrl = "https://www.reddit.com"
UserAgent = "{}: v{} (by /u/{})".format(Platform,Version,Author)
Amp = "%26"

class UrlTools(object):

	def __init__(self):
		pass

	def genDataString(self,**kwargs):
		data = urllib.urlencode(kwargs)
		return data

	def getPage(self,url,dataMap,headers):
		data = self.genDataString(**dataMap)
		req = urllib2.Request(url+"?"+data,headers=headers)
		f = urllib2.urlopen(req)
		self.page = json.loads(f.read())
		return self.page

class SubListing(UrlTools):

	def __init__(self,sub_base,limit=None,**kwargs):
		if limit is None:
			self.limit = 25
		else:
			self.limit = limit
		self.base = sub_base+".json"
		self.head = {'User-Agent':UserAgent}
		self.dataMap = {'limit': self.limit, 
				   		'before': 'None', 
				   		'after': 'None'}
		self.dataMap.update(kwargs)
		self.url = SiteUrl+self.base
		self.page = self.getPage(self.url,self.dataMap,self.head)
		self.state = {'before':self.page['data']['before'],
					  'after':self.page['data']['after']}
		self.dataMap.update(self.state)

	def updateState(self):
		self.state['before'] = self.page['data']['before']
		self.state['after'] = self.page['data']['after']

	def updateDataMap(self,**kwargs):
		self.dataMap.update(kwargs)

	def nextPage(self):
		self.dataMap['before'] = 'None'
		self.page = self.getPage(self.url,self.dataMap,self.head)
		self.updateState()
		self.updateDataMap(**self.state)

	def prevPage(self):
		self.dataMap['after'] = 'None'
		self.page = self.getPage(self.url,self.dataMap,self.head)
		self.updateState()
		self.updateDataMap(**self.state)


if __name__ == "__main__":
	num_pages = 2
	f = SubListing(sub_base="/r/esist/top",limit=10,t="all")
	for p in range(num_pages):
		for listing in f.page['data']['children']:
			print listing['data']['author']
		f.nextPage()
