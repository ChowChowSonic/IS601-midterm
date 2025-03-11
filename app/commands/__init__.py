"""Classes for commands"""
from typing import List
import pandas as pd
import os 
class Command:
	"""Abstract class that represents a command and what it can do"""
	def __init__(self):
		pass

	def execute(self, args:list[str]):
		"""Executes the command"""
		raise NotImplementedError("Command is an abstract class!")

class MenuCommand(Command):
	"""Lists all other commands"""
	def __init__(self, plugins:list[str]):
		self.plugins = plugins

	def execute(self, args):
		for x in self.plugins:
			print(x)

class HistoryCommand(Command):
	"""Command for saving and viewing history"""
	path = ""
	def __init__(self, path):
		HistoryCommand.path = path 
	@classmethod
	def add_to_history(cls, item: List[str], cmd:str):
		"""Adds a command to the history"""
		data={"Command": cmd} 
		for x in enumerate(item):
			data[x]=[item[x[0]]]
		df = pd.DataFrame(data, index=["column"])
		with open(HistoryCommand.path, 'a', encoding='utf-8') as file: 
			df.to_csv(HistoryCommand.path, mode='a', header=False, index=False)

	def execute(self, args:List[str]=[]):
		"""prints the entire history"""
		with open(HistoryCommand.path, 'r', encoding='utf-8') as file:
			lines = file.readlines()
			try:
				val=int(args[0])
				print(lines[val].replace(',', ' '))
				return
			except ValueError:
				HistoryCommand.clear_history()
			except IndexError:
				for x in lines:
					print(x.replace(',', ' '))

	@staticmethod
	def clear_history():
		"""Clears the history"""
		with open(HistoryCommand.path, 'w', encoding='utf-8'):
			pass

class CommandHandler:
	"""Handles commands"""
	def __init__(self):
		self.commands = {}

	def register_command(self, name: str, cmd: Command):
		"""Regsiters a command and associates it with a name"""
		self.commands[name]=cmd

	def execute_command(self, name:str, args:list[str]):
		"""Executes a command with a specified name and a list of args"""
		self.commands[name].execute(args)
