This is my midterm project for IS601-004: Web Systems Design
# Setting up 
Begin by cloning the respository
```
git clone && cd ./IS601-midterm
```
After cloning, install all dependencies from the requirements file
```
pip install -r requirements.txt
```
# Running the project
This project can be run with the following command:
```
python main.py [ARG1, ARG2, ARG3, ...] [COMMAND]
``` 
If no args are supplied, the project goes into REPL mode and accepts commands until one of the following conditions are met
 - Input reaches end-of-file (I.E. data is piped into the command)
 - The user enters an empty string
 - The user enters "exit"

# Built-in commands
The project has 3 built-in commands that cannot be deleted or modified: 
 - history
	- clear history - clears the history
	- [1 | 2 | 3 | ... | N ] get history - prints the N-th command executed
	- [1 | 2 | 3 | ... | N ] delete history - deletes the N-th command from the history
 - exit
 - menu 

# Plugins
This project supports plugins as well to further extend the application's usefulness. All plugins are stored in the `plugins/` folder. By default, the project comes with 4 plugins for addition, subtraction, multiplication and division. Each of these commands accepts two numbers as arguments and prints their result. 

# Building your own plugins
To build your own plugin, create a folder within the plugins folder, and make a file named `__init__.py`. Inside of the `__init__.py` file should be a class with the same name as the folder, but with a capitalized letter as the first character. This class should extend the built in `command` class that is provided by the project, and have an `execute(args:List[str])` function. Here is an example custom command & folder directory to build off of: 
```
plugins/
   | add/
   | divide/
   | multiply/
   | subtract/
   | customPlugin/ 
         | __init__.py
```
```#python
"""Contents of customPlugin/__init__.py"""
from app.commands import Command

class CustomPlugin(Command):
	def __init__(self):
		#do whatever here

	def execute(args:List[str] = []): 
		#this is run when you execute the command from the command line
```

# Design patterns & Implementation
An optional REPL (OREPL) method was chosen over a standard REPL method because I feel it provides the most convienence to the end user. OREPL allows users to run their code in a standard REPL format while also testing single commands via the command line. 

Additionally, the OREPL method handles pipes extremely well; just as well as a standard REPL does. When a pipe ends, an EOF error is thrown, which the user can handle by surrounding the REPL's loop with a single try-catch (using EAFP). Preformance is minimally impacted by the optionality as it adds in exactly ONE comparison check at the very beginning of execution. 

The app's command interface was implemented as an abstract object. This is because the `Command` class (it's really more like an interface from Java) is not supposed to do anything on its own, it simply defines the functionality that its child classes must have. Because of this, `Command.execute([args...])` throws an error if it is called. 

I used a singleton object to retrieve environment variables from the environment. It never made sense to me, in the original implementation, that each instance of `App` had its own copy of the environment variables. This was especially apparent when all of the instances would draw from the exact same .env file. Because of this I changed the implementation to all draw upon a single object any time I need access to an environment variable 

Inside of the app class I indirectly use a factory via Python's getAttr() function. This function allows me to retrieve an instance of each plugin's `Command`-extension class using only the name of the plugin, in a manner identical to a factory.

I used a facade pattern mixed with a singleton implementation over Pandas's implementation. As powerful of a tool as Pandas is, we were only using it to manage a single CSV containing all of the history. Because of this we could effectively lose most of Pandas's functionality with no detriment to us. So I invented a simpler implementation that goes over the existing library's code to make things easier to manage. Additionally, the singleton implementation makes the history management easier as I can "instanciate" (read: get a reference to) as many historymanager objects as i need and still have all of them write to the same file.