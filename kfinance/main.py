from .code import (get_stock_code)
from .naver import (Naver)
from .utils import (stock_loader)
from .utils import (save_csv)


def GetStockCode(stock_name):
	return get_stock_code(stock_name)

def GetStockData(stock_code):
	try:
		ret = Naver(stock_code).FromFinanceNaver()
	except:
		ret = stock_loader(stock_code)
	return ret
	
def StockData(stock_name):
	return Naver(get_stock_code(stock_name)).FromFinanceNaver()
	
def SaveCSV(stock_data, stock_name=None, stock_code=None):
	if stock_name!=None:
		return save_csv(stock_data, stock_name=stock_name)
	elif stock_code!=None:
		return save_csv(stock_data, stock_code=stock_code)
	return save_csv(stock_data)

# Will be removed
def FastReader(stock_name):
	return stock_loader(get_stock_code(stock_name))