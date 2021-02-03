import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
from io import StringIO
import tqdm


class Naver:
	def __init__(self, stock_code):
		self.__MAXNUM = 100000
		self.code = stock_code

	def FromFinanceNaver(self):
		# 페이지 수 확보 
		url = 'http://finance.naver.com/item/sise_day.nhn?code='+str(self.code)
		daySource = BeautifulSoup(urlopen(url).read(), "html.parser")
		PageNav = daySource.find_all("table", align="center")
		MaxPageSection = PageNav[0].find_all("td", class_="pgRR")
		MaxPageNum = int(MaxPageSection[0].a.get('href')[-3:])
		
		# 저장 공간 
		stock_data = pd.DataFrame()
		
		# 데이터 로드 
		for page in tqdm.tqdm(range(1,  MaxPageNum+1)):
			pg_url = '{url}&page={page}'.format(url=url, page=page) 
			stock_data = stock_data.append(pd.read_html(pg_url, header=0)[0], 
										   ignore_index=True)
			
		# 전처리 
		stock_data = stock_data.dropna()
		stock_data = stock_data.rename(columns= {'날짜': 'Date', 
												 '종가': 'Close', 
												 '전일비':'Change', 
												 '시가': 'Open', 
												 '고가': 'High', 
												 '저가': 'Low', 
												 '거래량':'Volume'})
		stock_data = stock_data.sort_values(by=['Date'], ascending=True)
		stock_data.set_index(['Date'], inplace=True)
		
		return stock_data