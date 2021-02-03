import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import datetime

# 삭제 예정 
def stock_loader(stock_code, start=None, end=None):
    # Load time info
    now   = datetime.now()
    if start==None:
        start = datetime(1996, 1, 1)
    if end==None:
        end   = now # datetime(2019, 5, 29)
		
    try:
        data = web.DataReader(name=stock_code+".KS", 
                              data_source="yahoo", 
                              start=start, end=end)
        print("If you want more, use 'get_from_naver'.")
        print("But it is slower than this.")
    except:
        print("DataSourceError: pandas_datareader's data source is not found.")
        data = pd.DataFrame()

    # 전처리 
    # stock_data = np.array(data.values[:-1, 1:].astype(np.float))
    # stock_data[np.isnan(stock_data)] = 0 # nan to zero 
    
    return data
	
def save_csv(data, stock_name=None, stock_code=None):
	now = datetime.now()
	dataframe = pd.DataFrame(data)
	if type(stock_name)==str:
		dataframe.to_csv(now.strftime("%Y%m%d-")+
						 stock_name+".csv",
						 header=True, index=True)
	elif type(stock_code)==str:				 
		code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?\
							   method=download&searchType=13', header=0)[0]
		code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
		ind = np.where(code_df['종목코드']==stock_code)
		dataframe.to_csv(now.strftime("%Y%m%d-")+
						 code_df['회사명'][ind[0][0]]+".csv",
						 header=True, index=True)
	else:
		dataframe.to_csv(now.strftime("%Y%m%d-")+
						 "StockData.csv",
						 header=True, index=True)