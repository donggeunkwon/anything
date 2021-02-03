import os

def __setup__():
	__package__ = ['pandas'
				  ,'numpy'
				  ,'pandas_datareader'
				  ,'datetime'
				  ,'urllib'
				  ,'re'
				  ,'requests'
				  ,'io'
				  ,'bs4']
				  
	for package in __package__:
		try:
			exec('import ' + package)
		except:
			os.system('pip install '+package)
