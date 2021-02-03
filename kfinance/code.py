from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import numpy as np

def get_stock_code(stock_name):
	# Check the type 
	if type(stock_name) != str:
		print("Stock name is not String type data.")
		return -1
	
	code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?\
						   method=download&searchType=13', header=0)[0] 
	code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
	code_df = code_df[['회사명', '종목코드']]
	
	# 영문 소문자 보정 
	stock_name = ''.join([i.capitalize() for i in stock_name])
	
	try:
		ind = np.where(code_df['회사명']==stock_name)
		stock_code = code_df['종목코드'][ind[0][0]]
	except:
		print("There are no stock name: "+stock_name)
		print("Did you find :")
		namelist = code_df['회사명'].to_numpy()
		namelist.sort()
		namelist = np.array([i[0] for i in namelist])
		ind = np.where(namelist==stock_name[0])
		for i in ind[0]:
			print(code_df['회사명'][i], end='/')
		return -1

	return stock_code