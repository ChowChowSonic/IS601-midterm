"""This is the class for the main command handler class """
import logging.config
import logging
import os
import sys
import importlib.util
from dotenv import load_dotenv
from app.commands import CommandHandler, MenuCommand

class App:
	"""The main class responsible for loading all plugins and handling commands"""
	def __init__(self):
		"""Initializer for class"""
		os.makedirs("logs", exist_ok=True)
		self.handler = CommandHandler()
		load_dotenv()
		self.settings = dict(os.environ.items())
		if os.path.exists(self.get_env("LOGGINGPATH")):
			logging.config.fileConfig(self.get_env("LOGGINGPATH"), disable_existing_loggers=False)
		logging.info("App started")

	def get_env(self, name:str):
		"""Returns an environment variable from the .env file"""
		return self.settings.get(name, None)

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
			except FileNotFoundError as e:
				logging.exception("Failed to load plugin %s: %s", format=(str(entry), str(e)))
		return modules

	def start(self):
		"""Loads all plugins"""
		plugins = self._import_plugins()
		for k in plugins:
			self.handler.register_command(k, getattr(plugins[k], k)())
			logging.info("Loaded plugin %s", format=k)
		self.handler.register_command("menu", MenuCommand(plugins.keys()))
		logging.info("Loaded menu plugin")

	def execute_command(self, cmd: str, args: list[str]):
		"""Executes a command with specified args"""
		logging.info("Executed command %s with args %s", format=(cmd, args))
		self.handler.execute_command(cmd, args)
