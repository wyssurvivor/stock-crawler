# -*- Encoding: utf-8 -*-
import os
from os.path import join,exists
import time
import request
import settings
import re
import persistency
import redis

block_pattern=re.compile(r'<a[^>]+href="bk_\d+\.shtml" .*</a>')
stock_pattern=re.compile(r'<a[^>]+href="/cn/\d+/index\.shtml" .*</a>')

def makeDir():
    for path in settings.crawl_paths:
        if not exists(path):
            os.makedirs(path)

def makeFileName(crawl_type,crawl_id=0):
    path=join(settings.cache_root,crawl_type)
    return join(path,crawl_type+str(crawl_id))

def clearRedis():
    r=redis.StrictRedis(**settings.redis_con)
    r.delete(settings.block_info_key)
    r.delete(settings.stock_info_key)

def grabBlockInfo():
    url=settings.blockurl.format("")
    content=request.doRequest(url,headers=settings.block_request_headers,filename=makeFileName("block"))
    blockset=set(block_pattern.findall(content))
    blockid_pattern=re.compile(r'bk_(\d+)')
    blockname_pattern=re.compile(ur'[\u4e00-\u9fa5][\u4e00-\u9fa5A-Za-z、]+')
    blockinfos=[]
    for b in blockset:
        rawcontent=b.decode('utf-8')
        block_id=blockid_pattern.findall(rawcontent)
        block_name=blockname_pattern.findall(rawcontent)
        blockinfos.append({"block_id":block_id[0],"block_name":block_name[0]})
    return blockinfos

def grabStockInfoFromBlockInfo(blockinfos):
    stockinfos=[]
    stockid_pattern=re.compile(r'/(\d+)/')
    #stockname_pattern=re.compile(ur'>([\u4e00-\u9fa5A-Za-z、*]+)')
    stockname_pattern=re.compile(r'>(.*)<')
    for blockinfo in blockinfos:
        url=settings.blockurl.format("_"+str(blockinfo['block_id']))
        content=request.doRequest(url,headers=settings.block_request_headers,filename=makeFileName('stock',blockinfo['block_id']))
        if content==None:
            continue
        stockset=set(stock_pattern.findall(content))
        for stock in stockset:
            rawcontent=stock.decode('utf-8')
            stock_id=stockid_pattern.findall(rawcontent)
            stock_name=stockname_pattern.findall(rawcontent)
            print rawcontent,blockinfo['block_id']
            print stock_id[0],stock_name[0]
            stockinfos.append({"block_id":blockinfo['block_id'],"stock_id":stock_id[0],"stock_name":stock_name[0]})
    print len(stockinfos)
    return stockinfos

def grabStockPerformRealTime(stockid):
    now=int(time.time())
    url=settings.stockperformurl % (stockid.substring(3),stockid,str(now))
    print url
    perform_request_headers=settings.block_request_headers
    perform_request_headers['Host']='hq.stock.sohu.com'
    perform_request_headers['Referer']=settings.stockurl % stockid


def grabBlockInfoRoutine():
    blockinfos=grabBlockInfo()
    persistency.saveBlockInfos(blockinfos)
    return blockinfos

def grabStockInfoRoutine():
    blockinfos=grabBlockInfoRoutine()
    stockinfos=grabStockInfoFromBlockInfo(blockinfos)
    persistency.saveStockInfos(stockinfos)
    return stockinfos

def prepare():
    makeDir()
    clearRedis()

if __name__=="__main__":
    prepare()
    grabStockInfoRoutine()
    #blockinfos=grabBlockInfo()
    #persistency.saveBlockInfos(blockinfos)
    #stockinfos=grabStockInfoFromBlockInfo([{'block_id':1891,'block_name':'银行'},{'block_id':1879,'block_name':'房地产'}])
    #stockinfos=grabStockInfoFromBlockInfo(blockinfos)
    #persistency.saveStockInfos(stockinfos)
    #stockinfos=grabStockInfoFromBlockInfo([{'block_id':2054,'block_name':'what'}])
























