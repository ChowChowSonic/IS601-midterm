"""Classes for commands"""
from typing import List
import pandas as pd
import logging
from app.historymanager import HistoryManager 
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
		"""Lists all other commands"""
		for x in self.plugins:
			print(x)

class HistoryCommand(Command):
	"""Command for saving and viewing history"""
	def __init__(self):
		self.mgr = HistoryManager()
	
	def execute(self, args:List[str]=[]):
		"""prints the entire history. Avoids LBYL by using EAFP"""
		arg1=None
		try: 
			a1=args[0]
			possibilities={
				"clear":"clear", 
			}
			possibilities[a1]
			self.mgr.clear_history()
			return
		except KeyError:
			logging.info("a1 parsed int successfully")
			arg1=int(a1)
		except IndexError: 
			logging.info("loading history")
			self.mgr.loadHistory()
			return
		
		try:
			a2 = args[1]
			possibilities = {
				"delete":self.mgr.delete_command, 
				"get":self.mgr.load_command 
			}
			x = possibilities[a2](arg1)
			if x is not None:
				print(x)
		except KeyError:
			logging.error("Unknown command passed to history %s", a2)
			print("Unknown command passed to history", a2)
			return

class CommandHandler:
	"""Handles commands"""
	def __init__(self):
		self.commands = {}

	def register_command(self, name: str, cmd: Command):
		"""Regsiters a command and associates it with a name"""
		self.commands[name]=cmd

	def execute_command(self, name:str, args:list[str]):
		"""Executes a command with a specified name and a list of args"""
		logging.info("command & args passed to commandHandler: %s %s", name, args)
		self.commands[name].execute(args)
