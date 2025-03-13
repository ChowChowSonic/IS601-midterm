"""Implements a history manager using a facade interface over Pandas"""
from typing import List 
import pandas as pd 
from app.env import Env
from app.singleton import Singleton
class HistoryManager(Singleton):
	_df = None
	def __init__(self):
			if HistoryManager._df is not None: 
				return 
			env = Env()
			file = env.getenv("HISTORYPATH")
			try:
				HistoryManager._df = pd.read_csv(file, header=None)
			except pd.errors.EmptyDataError as e:	#pragma: no cover
				HistoryManager._df = pd.DataFrame([], columns=[1,2,3,4,5,6,7,8,9]) #pragma: no cover

	def append(self, cmd:str, item:List[str]): 
		"""Adds a command to the history. This method is classed 
		because there will only be one history file, 
		(accessed via a class variable) so we don't need to make it 
		instance based. Additionally, if we make this
		instance based, then there will be no way to call this method
		should we cast the history command to its superclass"""
		newdata=pd.DataFrame( [[cmd, *item]], columns=range(len(item)+1))
		HistoryManager._df = pd.concat([HistoryManager._df, newdata], ignore_index=True, axis=0, copy=False)

	def write_history(self):
		file = Env().getenv("HISTORYPATH")
		with open(file, 'w', encoding='utf-8') as file: 
			HistoryManager._df.to_csv(file, header=False, index=False)

	def delete_command(self, n):
		"""Deletes a single command from the history"""
		HistoryManager._df.drop([n], inplace=True)
	def load_command(self, n:int): 
		"""Loads a single command from the history"""
		return HistoryManager._df[n]
	def clear_history(self):
		"""Clears the history"""
		HistoryManager._df = pd.DataFrame(columns=range(10))

	def loadHistory(self): 
		"""Loads the entire history"""
		print(HistoryManager._df)
