import redis
from mysql import MySQL
from settings import redis_con,block_info_key,stock_info_key

m=MySQL()
r=redis.StrictRedis(**redis_con)



def saveBlockInfo(blockinfo):
	if r.sismember(block_info_key,blockinfo['block_id'])==0:
		m.insert('block_info',blockinfo)
		r.sadd(block_info_key,blockinfo['block_id'])
	return 1

def saveBlockInfos(blockinfos):
	count=0
	for blockinfo in blockinfos:
		if saveBlockInfo(blockinfo):
			count=count+1
	return count

def saveStockInfo(stockinfo):
	if r.sismember(stock_info_key,stockinfo['stock_id'])==0:
		m.insert('stock_info',stockinfo)
		r.sadd(stock_info_key,stockinfo['stock_id'])
	return 1

def saveStockInfos(stockinfos):
	count=0
	for stockinfo in stockinfos:
		if saveStockInfo(stockinfo):
			count=count+1
	return count

if __name__=="__main__":
	#saveBlockInfos([{'block_id':1891,'block_name':'bank'},{'block_id':1879,'block_name':'house'}])
	saveStockInfos([{'stock_id':000001,'block_id':1897},{'stock_id':000002,'block_id':1897},{'stock_id':000003,'block_id':1891}])