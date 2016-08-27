# -*- Encoding: utf-8 -*-
import redis
import re
import requests
import random
import time
import cchardet
from settings import redis_con,delay_bottom,delay_top

#import sys  
#reload(sys)  
#sys.setdefaultencoding('utf8') 

r=redis.StrictRedis(**redis_con)
# todo : add logs

def wait(f):
	lock_name="http-lock"

	def _wrap_func(*args,**kwargs):
		t=r.ttl(lock_name)
		if t>0:
			print "waiting"
			time.sleep(t)
		delay=int(random.uniform(delay_bottom,delay_top))
		r.setex(lock_name,delay,'locking')
		return f(*args,**kwargs)
	return _wrap_func

@wait
def doRequest(url,timeout=2,method='GET',filename=None,headers=None):
	if method=='GET':
		return doGet(url,timeout,filename,headers)
	else:
		return doPost(url,timeout,filename,headers)


def doGet(url,timeout=2,filename=None,headers=None):
	try:
		res=requests.get(url,timeout=timeout,headers=headers)
	except requests.exceptions.Timeout:
		print "time out while fetch %s" % url
		return None
	except requests.exceptions.ConnectionError:
		print "failed to establish a new connection"
		return None
	print url
	encoding=cchardet.detect(res.content)['encoding']
	content=res.content.decode(encoding).encode('utf-8')
	if content:
			with open(filename,'w') as f:
				f.write(content)
	else:
		print "content is null"
	return content

def doPost(url,timeout=2,filename=None,headers=None):
	pass

