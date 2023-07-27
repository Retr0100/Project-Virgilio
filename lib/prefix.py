from colorama import Fore,Back
import inspect
import time


def Log(string:str):
    callstack = inspect.stack()[1]
    caller = str(inspect.getmodule(callstack[0])).split("\\")[-1]
    prfx=(Fore.GREEN + f"(in module {caller[:-2]}) " + time.strftime("%H:%M:%S UTC LOG", time.localtime()) + Back.RESET + Fore.WHITE)
    prfx = (prfx + " | ")
    log = prfx + string
    return log


print(Log("ciao"))