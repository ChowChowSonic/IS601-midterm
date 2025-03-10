

class Command: 
	def __init__(self):
		pass

	def execute(self, args:list[str]):
		raise NotImplementedError("Command is an abstract class!")
	
class MenuCommand(Command):
	def __init__(self, plugins:list[str]):
		self.plugins = plugins

	def execute(self, args):
		for x in self.plugins: 
			print(x)


class CommandHandler: 

	def __init__(self):
		self.commands = {}


	def register_command(self, name: str, cmd: Command):
		self.commands[name]=cmd

	def execute_command(self, name:str, args:list[str]): 
		self.commands[name].execute(args) 