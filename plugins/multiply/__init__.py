"""Command for multiplication"""
from app.commands import Command
class Multiply(Command):
	"""multiplies two numbers passed as args"""
	def __init__(self):
		pass
	def execute(self, args:list[str]):
		"""Actually multiplies the numbers and prints the result"""
		print("The result of",args[0],"multiply",args[1],"is equal to",int(args[0])*int(args[1]))
		# p.start()
		# p.join()
