# -*- coding: utf-8 -*-
import MySQLdb
from settings import mysql_con

class MySQL:
	def __init__(self):
		try:
			self.conn=MySQLdb.connect(**mysql_con)
			self.conn.autocommit(False)
			self.conn.set_character_set(mysql_con['charset'])
			self.cur=self.conn.cursor()
		except MySQLdb.Error as e:
			print ("Mysql Error, %d:%s" % (e.args[0],e.args[1]))
			# add log

	def __del__(self):
		self.close()

	def selectDb(self,Db):
		try:
			self.conn.select_db(db)
		except MySQLdb.Error as e:
			print ("Mysql Error, %d:%s" % (e.args[0],e.args[1]))

	def queryStr(self,sql):
		try:
			n=self.cur.execute(sql)
			return n
		except MySQLdb.Error as e:
			print ("MySQL Error:%s\nSQL:%s" % (e,sql))
			return 0

	def query(self,table_name,condition):
		_condition=[]
		for key in condition.keys():
			_condition.append("%s='%s'" % (key,condition[key]))
		_prefix="".join(["select * from ",table_name])
		if len(_condition)>0:
			sql="".join([_prefix," where "," and ".join(_condition)])
		else:
			sql=_prefix
		self.execute(sql)

	def fetchRow(self):
		result=self.cur.fetchone()
		return result

	def fetchAll(self):
		result=self.cur.fetchall()
		desc=self.cur.description
		d=[]
		for inv in result:
			_d={}
			for i in range(0,len(inv)):
				_d[desc[i][0]]=str(inv[i])
			d.append(_d)
		return d

	def insert(self,table_name,data):
		columns=data.keys()
		_prefix="".join(['INSERT INTO `',table_name,'`'])
		_fields=",".join(["".join(['`',column,'`']) for column in columns])
		_values=",".join(["%s" for i in range(len(columns))])
		_sql="".join([_prefix,"(",_fields,") values (",_values,")"])
		_params=[data[key] for key in columns]
		return self.executeParam(_sql,tuple(_params))

	def update(self,table_name,data,condition):
		_fields=[]
		_condition=[]
		_prefix="".join(["update `",table_name,"` SET "])
		for key in data.keys():
			_fields.append("%s='%s'" % (key,data[key]))
		for key in condition.keys():
			_condition.append("%s='%s'" % (key,condition[key]))
		_sql="".join([_prefix,",".join(_fields)," where "," and ".join(_condition)])
		return self.execute(_sql)

	def delete(self,table_name,condition):
		_condition=[]
		_prefix="".join(["delete from `",table_name,'` where '])
		for key in condition.keys():
			_condition.append("%s='%s'" % (key,condition[key]))
		_sql="".join([_prefix," and ".join(_condition)])
		return self.execute(_sql)

	def execute(self,sql):
		try:
			n=self.cur.execute(sql)
			self.commit()
			return n
		except MySQLdb.Error as e:
			print ("Mysql Error, %d:%s" % (e.args[0],e.args[1]))
			self.rollback()
			return 0

	def executeParam(self,sql,param):
		try:
			n=self.cur.execute(sql,param)
			self.commit()
			return n
		except MySQLdb.Error as e:
			print ("Mysql Error, %d:%s" % (e.args[0],e.args[1]))
			self.rollback()
			return 0

	def getLastInsertId(self):
		return self.cur.lastrowid

	def rowcount(self):
		return self.cur.rowcount

	def commit(self):
		self.conn.commit()

	def rollback(self):
		self.conn.rollback()

	def close(self):
		self.cur.close()
		self.conn.close()

if __name__=="__main__":
	mysql=MySQL()
	mysql.queryStr('select * from block_info')
	print mysql.fetchRow()
	data={
		'block_id':'6',
		'block_name':'test6'
	}
	#mysql.insert('block_info',data)
	#mysql.queryStr('select * from block_info')
	#print mysql.fetchAll()
	data2={
		'block_name':'updated',
	}
	#mysql.update('block_info',data2,{'block_id':6})
	#mysql.queryStr('select * from block_info')
	#print mysql.fetchAll()
	#mysql.delete('block_info',{'block_id':6})
	#mysql.queryStr('select * from block_info')
	#print mysql.fetchAll()
	mysql.query('block_info',{'block_id':2})
	print mysql.fetchAll()
