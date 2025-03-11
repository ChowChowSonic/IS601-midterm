"""Classes for commands"""
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
