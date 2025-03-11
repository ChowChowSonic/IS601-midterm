"""Command for division"""
from app.commands import Command
class Divide(Command):
	"""divides two numbers passed as args"""
	def __init__(self):
		pass
	def execute(self, args:list[str]):
		"""Actually divides the numbers and prints the result"""
		print("The result of",args[0],"divide",args[1],"is equal to",int(args[0])//int(args[1]))
		# p.start()
		# p.join()
