"""Command for addition"""
from app.commands import Command
class Add(Command):
	"""Adds two numbers passed as args"""
	def __init__(self):
		pass
	def execute(self, args:list[str]):
		"""Actually does the addition, printing the result"""
		print("The result of",args[0],"add",args[1],"is equal to",int(args[0])+int(args[1]))
		# p.start()
		# p.join()
