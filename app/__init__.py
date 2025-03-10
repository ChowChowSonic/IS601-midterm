import logging.config
from app.commands import CommandHandler, MenuCommand
from dotenv import load_dotenv
import os, sys, importlib.util
import logging 

class App:
	def __init__(self):
		os.makedirs("logs", exist_ok=True)
		self.handler = CommandHandler()
		load_dotenv()
		self.settings = {key:value for key, value in os.environ.items()}
		if os.path.exists(self.get_env("LOGGINGPATH")):
			logging.config.fileConfig(self.get_env("LOGGINGPATH"), disable_existing_loggers=False)
		logging.info("App started")
		
	def get_env(self, name:str): 
		return self.settings.get(name, None) 

	def _import_plugins(self, plugins_dir:str="plugins"):
		plugins_path = os.path.abspath(plugins_dir)
		modules = {}
		sys.path.insert(0, os.path.abspath(os.getcwd()))
		for entry in os.listdir(plugins_path):
			entry_path = os.path.join(plugins_path, entry)
			if os.path.isdir(entry_path) and os.path.isfile(
                os.path.join(entry_path, "__init__.py")
            ):
				module_name = entry  # Use the subdirectory name as the module name
				init_py = os.path.join(entry_path, "__init__.py")
				spec = importlib.util.spec_from_file_location(
					module_name, init_py, submodule_search_locations=[entry_path]
				)
				if spec and spec.loader:
					module = importlib.util.module_from_spec(spec)
					spec.loader.exec_module(module)
					modules[module_name] = module
		return modules
    
	def start(self):
		plugins = self._import_plugins()
		for k in plugins:
			self.handler.register_command(k, getattr(plugins[k], k)())
		self.handler.register_command("menu", MenuCommand(plugins.keys()))

	def execute_command(self, cmd: str, args: list[str]): 
		logging.info(f"Executed command {cmd} with args {args}")
		self.handler.execute_command(cmd, args)