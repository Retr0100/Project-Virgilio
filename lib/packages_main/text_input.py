"""The input file for the text."""
import json
import sys
import unicodedata

from lib.packages_utility.logger import logging
from lib.packages_utility.utils import Utils

# ----- File to take the input by the console -----

class TextInput:
    """Class that takes a text as an argument and returns it in lowercase, without accents or special characters."""
    def __init__(self,word_activation) -> None:
        """Init func.

        Args:
            word_activation (str): The word for the activation of Virgil
        """
        self.data_empty = {
            None:True
            }
        self.utils = Utils()

        self.word_activation = word_activation

    def copy_data(self,command:str):
        """Copy data from a command line.

        and return it as string or list of strings if needed for further processing in other functions.

        Args:
            command (str): Command to copy in the file
        """
        data = {
            command:False
            }
        logging.debug(f" data sended - {data}")
        with open("connect/command.json", 'w',encoding="utf8") as comandi:
            json.dump(data, comandi,indent=4)

    def text(self):
        """The main file for recover the command from text."""
        command = ""
        logging.info(" start input function")
        self.utils.clean_buffer(data_empty=self.data_empty,file_name="command")
        status  = True
        while status:
            command = str(
                input("Enter the command or question you need (use key word Virgilio): ")).lower()
            command = unicodedata.normalize('NFKD', command)
            command = command.encode('ascii', 'ignore').decode('ascii')
            if self.word_activation in command:
                logging.debug(" command speech correctly ")
                self.copy_data(command)
                if "spegniti" in command:
                    status = False
            else:
                logging.warning("Remember to use the key word")
        sys.exit()
