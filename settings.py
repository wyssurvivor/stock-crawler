from os.path import join,dirname

dirbase=dirname(__file__)
cache_root=join(dirbase,'cache')

db=8

# crawl types 
crawl_types=["block","stock"]
crawl_paths={join(cache_root,name) for name in crawl_types}

# redis connection
redis_con={
	"host":"127.0.0.1",
	"port":6379,
	"db":8,
}

# redis keys
block_info_key="sohu:blockinfo"
stock_info_key="sohu:stockinfo"

# request headers
block_request_headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Cookie':'vjuids=b7562ad5b.152056d1774.0.b91df181; sohutag=8HsmeSc5NCwmcyc5NSwmYjc5NCwmYSc5NCwmZjc5NCwmZyc5NCwmbjc5NCwmaSc5NCwmdyc5NCwmaCc5NCwmYyc5NCwmZSc5NCwmbSc5NCwmdCc5NH0; IPLOC=CN1100; beans_dmp={"admaster":1470459542,"shunfei":1470459542,"reachmax":1471685261,"lingji":1470459542,"yoyi":1470459542,"ipinyou":1470459542,"ipinyou_admaster":1470459542,"jingzan":1470459542,"miaozhen":1470459542,"aodian":1470459542}; beans_dmp_1601031059421915=1471685262431; SUV=1601031059421915; beans_dmp_done=1; BIZ_MyLBS=cn_600187%2C%u56FD%u4E2D%u6C34%u52A1%7Ccn_000839%2C%u4E2D%u4FE1%u56FD%u5B89%7Ccn_000002%2C%u4E07%u79D1%uFF21; vjlast=1451789982.1471741050.11',
    'Host':'q.stock.sohu.com',
    'Referer':'http://q.stock.sohu.com/cn/ph.shtml',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}

# request urls
blockurl='http://q.stock.sohu.com/cn/bk{}.shtml'
stockurl='http://q.stock.sohu.com/cn/{}/index.shtml'
stockperformurl='http://hq.stock.sohu.com/cn/{}/cn_{}-1.html?_={}'

# delays
delay_bottom=5
delay_top=10

# mysql connection
mysql_con={
	"host":"locahost",
	"port":3306,
	"user":"root",
	"passwd":"123456",
	"charset":"utf8",
	"db":"stock"
}

try:
	from local_settings import *
except Exception as e:
	pass