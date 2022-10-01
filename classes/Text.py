from colorama import Fore, init; init()

class Text:
    def __init__(self, text:str, color:str):
        self.text = text
        self.color = color

    def __str__(self) -> str:
        return f"{self.color}{self.text}{Fore.RESET}"