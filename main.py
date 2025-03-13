"""Main (driver) code """

import logging
import sys
from app import App
from app.historymanager import HistoryManager

def calculate_and_print(argv: list[str] = []) -> float | int:
    """
    Utilizes a REPL implementation to take several user commands when no arguments are supplied. 
    Wraps REPL implementaton in EAFP because we assume the user's input is going to be correct
    in most cases.  
    """
    try:
        app = App()
        app.start()
        if len(argv) == 0:
            app.execute_command("menu", [])
            ctr = 0
            x = " "
            while x not in {'', "exit"}:
                x = input()
                ctr += 1
                if x not in {'', "exit"}:
                    lst = x.strip().split(" ")
                    app.execute_command(lst[-1], lst[:-1])
        else:
            app.execute_command(argv[-1], argv[:-1])
    except ZeroDivisionError:
        print("An error occurred: Cannot divide by zero")
        logging.error("Attempted to divide by zero. Aborting...")
    except KeyError:
        print("Unknown operation:", argv[-1] if len(argv) > 0 else lst[-1])
        logging.error("Unknown operation passed: %s; Aborting...", argv[-1] if len(argv) > 0 else lst[-1])
    except ValueError:
        print(f"Invalid number input: {argv[0]} or {argv[1]} is not a valid number.")
        logging.error("Invalid number input entered: %s %s; Aborting...", argv[0], argv[1])
    except EOFError:
        # This is to be expected when we pipe stuff in. This is intended
        # behavior so there will be no errors to be logged because of that
        pass
    HistoryManager().write_history()

if __name__ == "__main__":
    calculate_and_print(sys.argv[1:])  # pragma: no cover
