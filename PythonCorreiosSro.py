#! -*- encoding:utf-8 -*- W
"""
Created on Jun 18 2012
@author Julio Silveira Melo
1.0.0
"""

import urllib
import urllib2
from bs4 import BeautifulSoup
import socket


class PythonCorreiosSro:
	
	def __init__(self, object_id=None):
		
		self.base_url = "http://websro.correios.com.br/sro_bin/txect01$.QueryList"

		if object_id:
			self.data = {'P_ITEMCODE' :'',
				'P_LINGUA': '001',
				'P_TESTE':'',
				'P_TIPO':'001',
				'P_COD_UNI': object_id.upper(),
				'Z_ACTION':'Pesquisar',
			}

	def process_request(self):
		query = urllib.urlencode(self.data)
		request = urllib2.Request(self.base_url, query)
		return request

	def response(self):
		timeout = 5
		socket.setdefaulttimeout(timeout)

		try:
			response = urllib2.urlopen(self.process_request())
		except urllib2.HTTPError, e:
			if e.code == 502:
				self.behind_proxy()
				response_behind_proxy = urllib2.urlopen(self.process_request())
				return response_behind_proxy.read()
		return response.read()

	def behind_proxy(self):
		proxy_support = urllib2.ProxyHandler({})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		return

	
	def beautify(self):
		data = {}
		page = self.response()
		soup = BeautifulSoup(page)
		table = soup.find('table')
		cols = [col.string for col in table.find_all('td')[3:]]
		data['status'] = cols

		return data

	@property
	def status(self):
		try:
			if self.beautify():
				data = self.beautify()
				return data['status']
		except AttributeError:
			data = []
			return data







