from colorama import Fore, init; init()

def colortext(text:str, color:str=Fore.WHITE) -> str:
    return f"{color}{text}{Fore.RESET}"