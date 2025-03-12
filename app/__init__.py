"""This is the class for the main command handler class """
import logging.config
import logging
import os
import sys
import importlib.util
from app.env import Env 
from app.commands import CommandHandler, MenuCommand, HistoryCommand

class App:
	"""The main class responsible for loading all plugins and handling commands"""
	def __init__(self):
		"""Initializer for class"""
		if os.path.exists(Env.getenv("LOGGINGPATH")):
			logging.config.fileConfig(Env.getenv("LOGGINGPATH"), disable_existing_loggers=False)
		os.makedirs("logs", exist_ok=True)
		self.handler = CommandHandler()

	def _import_plugins(self, plugins_dir:str="plugins"):
		""" Utilizes EAFP when traversing the plugins directory as we assume by
		default that all of the plugins follow the correct format"""
		plugins_path = os.path.abspath(plugins_dir)
		modules = {}
		sys.path.insert(0, os.path.abspath(os.getcwd()))
		for entry in os.listdir(plugins_path):
			entry_path = os.path.join(plugins_path, entry)
			try:
				module_name = entry
				init_py = os.path.join(entry_path, "__init__.py")
				spec = importlib.util.spec_from_file_location(
					module_name, init_py, submodule_search_locations=[entry_path]
				)
				if spec and spec.loader:
					module = importlib.util.module_from_spec(spec)
					spec.loader.exec_module(module)
					modules[module_name] = module
			except FileNotFoundError as e: #pragma: no cover
				logging.error("Failed to load plugin %s: %s", str(entry),str(e)) #pragma: no cover
		return modules

	def start(self):
		"""Loads all plugins"""
		plugins = self._import_plugins()
		for k in plugins:
			self.handler.register_command(k.lower(), getattr(plugins[k], k[0].upper()+k[1:])())
			logging.info("Loaded plugin %s", k)
		self.handler.register_command("menu", MenuCommand(plugins.keys()))
		logging.info("Loaded menu plugin")
		self.handler.register_command("history", HistoryCommand())
		logging.info("Loaded history plugin")

	def execute_command(self, cmd: str, args: list[str]):
		"""Executes a command with specified args"""
		self.handler.execute_command(cmd.lower(), args)
		logging.info("Executed command %s with args %s", cmd, args)
		HistoryCommand.add_to_history(args, cmd)
