"""This file take care of configuring the entire environment for the use of Virgilio."""
import os
import platform
import sys
import subprocess
import shutil
import colorama
import tomli
from tomlkit import parse, dumps
import pyfiglet


# --- CONST

SUCCESS_MESSAGE = colorama.Fore.GREEN + colorama.Style.BRIGHT +"\n ***** Successfully executed changes *****"

# ------ WINDOWS -------

def windows_function(path_directory):
    """Function to with command for Windows."""
    with open("launch_start.bat","w",encoding='utf-8')as file:
        file.write(f"python {path_directory}\\launch.py")
    source_path = f"{path_directory}\\setup\\launch_start.bat"
    current_user = os.getlogin()
    source_path = 'F:\\ProjectVirgil\\VirgilAI\\setup\\launch_start.bat'
    destination_folder = f'C:\\Users\\{current_user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    try:
        shutil.copy2(source_path, destination_folder)
    except OSError:
        print(colorama.Fore.RED+ colorama.Style.BRIGHT + '''
 Oops your antivirus doesn't like Virgilio to start automatically please
 give the green light to the antivirus to run the bat file (If you have
 any doubts about security I invite you to analyze the whole source code
 and check its security and if you still don't trust it you can simply
 don't run it at startup)''',flush=True)
    os.remove(source_path)

def modify_start_startup_win(launch_start):
    """This function is used for modifying the startup file of start.py.

    Args:
        launch_start (_type_): _description_
    """
    current_user = os.getlogin()
    if launch_start:
        try:
            destination_folder = f'C:\\Users\\{current_user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\launch_start.bat'
            os.remove(destination_folder)
        except FileNotFoundError:
            print("FILE NOT FOUND",flush=True)
    else:
        current_folder = os.getcwd()
        parent_folder = os.path.dirname(current_folder)
        windows_function(parent_folder)
    print(SUCCESS_MESSAGE,flush=True)
    update_toml("launch_start",not launch_start)

def modify_display():
    """This function is used for modifying the configuration of the display."""
    _,_,defaul_start,display_console = get_data()
    path = get_path()
    if(defaul_start in ('T','N') and display_console is not True):
        if platform.system() == "Windows":
            update_toml("display_console",not display_console)
            os.rename("../launch.pyw","../launch.py")
            windows_function(path)
            print(SUCCESS_MESSAGE,flush=True)
        else:
            linux_function(path,display=True)
            print(SUCCESS_MESSAGE,flush=True)
    elif(defaul_start in ('T','N') and display_console is True):
        print(colorama.Fore.RED + colorama.Style.BRIGHT +"\n You can't set the display to False with default startup to Text \n if you can set to display true first set the interface to text or remove the dafault ",flush=True)
    else:
        if platform.system() == "Windows":
            os.rename("../launch.py","../launch.pyw")
            windows_function(path)
            update_toml("display_console",not display_console)
            print(SUCCESS_MESSAGE,flush=True)
        else:
            linux_function(path,display=False)
            print(SUCCESS_MESSAGE,flush=True)

# ----- SYSTEM ------
def check_system() -> str:
    """Check on what platform the script was run on.

    Returns:
        str: the system used
    """
    if platform.system() == "Windows":
        return "W"
    if platform.system() == "Linux":
        return "L"
    return "N"

def get_data():
    """Get metadata from pyproject.toml.

    Returns:
        tupla: All the metadata neccesary for the setup
    """
    toml_path = '../pyproject.toml'
    with open(toml_path, "rb") as file:
        metadata = tomli.load(file)
        first_setup = metadata["tool"]["config_system"]["first_setup"]
        launch_start = metadata["tool"]["config_system"]["launch_start"]
        defaul_start = metadata["tool"]["config_system"]["defaul_start"]
        display_console = metadata["tool"]["config_system"]["display_console"]
        file.close()

    return first_setup,launch_start,defaul_start,display_console

def update_toml(params: str, new_value: str):
    """Update TOML file from params dictonary.

    Args:
        params (str): _description_
        new_value (str): _description_
    """
    file_path = "../pyproject.toml"
    with open(file_path,encoding='utf-8') as file:
        content = file.read()
    doc = parse(content)
    doc["tool"]["config_system"][params] = new_value
    new_content = dumps(doc)
    with open(file_path, "w",encoding='utf-8') as file:
        file.write(new_content)

def show_settings():
    """This function shows all settings."""
    _,launch_start,defaul_start,display_console = get_data()
    mss_list = ["The option for the launch start with the system is: ","The option for the default launch is: ","The option for the show of display is: ",]
    value = [launch_start,defaul_start,display_console]
    print(colorama.Fore.BLUE + colorama.Style.BRIGHT + "\n\t    ------ [SETTINGS] -------\n",flush=True)
    for mss in mss_list:
        print(colorama.Fore.CYAN + colorama.Style.BRIGHT + " - " + mss + colorama.Fore.GREEN + str(value[mss_list.index(mss)]),flush=True)

# ----- LINUX ------
def modify_start_startup_lin(launch_start,display):
    """Modify the start of Virgil on startup.

    Args:
        launch_start (_type_): _description_
        display (_type_): _description_
    """
    if launch_start:
        command = "echo  | crontab -"
        try:
            subprocess.run(command, shell=True,check=True)
        except subprocess.CalledProcessError as error:
            print(f"Error on Crontab: {error}",flush=True)
            update_toml("launch_start",not launch_start)
    else:
        linux_function(get_path,display=display)
        update_toml("launch_start",not launch_start)

def linux_function(path_directory=None,display=True):
    """Function to with command for Linux."""
    # PER LINUX GENERARE SOLO IL COMANDO E FARLO ESEGUIRE ALL UTENTE
    # Comando per aggiungere un lavoro Crontab che si esegue all'avvio
    if display:
        job = f"@reboot screen -dmS virgil /usr/bin/python3 {path_directory}/launch.py"
        print("\n" + colorama.Fore.RED +colorama.Style.BRIGHT +"For connect to the terminal execute this command: screen -r virgil",flush=True)
    else:
        job = f"@reboot /usr/bin/python3 {path_directory}/launch.py"

    command = f"echo {job} | crontab -"  # Comando completo
    try:
        subprocess.run(command, shell=True,check=True)
    except subprocess.CalledProcessError as error:
        print(f"Error on Crontab: {error}",flush=True)

# ---- FIRST START ------

def first_start(cli,parent_folder):
    """First start of the project.

    Args:
        cli (function): _description_
        parent_folder(str): The path for the script
    """
    print(f"\nCURRENT SYSTEM: [{platform.system()}]",flush=True)
     # PASS 1
    while True:
        sys.stdout.write(colorama.Fore.CYAN + colorama.Style.BRIGHT +
                        '''\n(-) 1. Do you want virgil to be started at system startup? (default no) (Y/N): ''')
        sys.stdout.flush()
        choise = sys.stdin.readline().strip().upper()
        if choise in ('N','Y'):
            break
        sys.stdout.write(colorama.Fore.RED + colorama.Style.BRIGHT +'\x1b[A' + '''(/) SELECT A VALID CHOISE'''+ " "*100 + '\r')
        sys.stdout.flush()

    sys.stdout.write(colorama.Fore.GREEN + colorama.Style.BRIGHT + '\x1b[A' + f"(-) 1. Do you want virgil to be started at system startup? (default no) (Y/N): {choise}" + '\r')
    sys.stdout.flush()

    if choise =="Y":
        update_toml("launch_start",True)
        cli(parent_folder)
    else:
        update_toml("launch_start",False)

    while True:
        sys.stdout.write(colorama.Fore.CYAN + colorama.Style.BRIGHT +
                        '''\n(-) 2. Do you want to specify a default interface type? (default no) (Y/N): ''')
        sys.stdout.flush()
        choise = sys.stdin.readline().strip().upper()
        if choise in ('N','Y'):
            break
        sys.stdout.write(colorama.Fore.RED + colorama.Style.BRIGHT +'\x1b[A' + '''(/) SELECT A VALID CHOISE'''+ " "*100 + '\r')
        sys.stdout.flush()

    sys.stdout.write(colorama.Fore.GREEN + colorama.Style.BRIGHT +'\x1b[A' + f"(-) 2. Do you want to specify a default interleaving type? (default no) (Y/N): {choise}" + '\r')
    sys.stdout.flush()
    if choise == 'Y':
        while True:
            sys.stdout.write(colorama.Fore.CYAN + colorama.Style.BRIGHT +
                            '''\n(-) 2.1 Text interface or voice interface? (T/R):''')
            sys.stdout.flush()
            choise = sys.stdin.readline().strip().upper()
            if choise in ('T','R'):
                break
            sys.stdout.write(colorama.Fore.RED + colorama.Style.BRIGHT +'\x1b[A' + '''(/) SELECT A VALID CHOISE'''+ " "*100 + '\r')
            sys.stdout.flush()

        sys.stdout.write(colorama.Fore.GREEN + colorama.Style.BRIGHT +'\x1b[A' + f"(-) 2.1 Text interface or voice interface? (T/R): {choise}" + '\r')
        sys.stdout.flush()
        update_toml("defaul_start",choise)

        if choise == 'R':
            # PASS 4
            while True:
                sys.stdout.write(colorama.Fore.CYAN + colorama.Style.BRIGHT +
                                '''\n(-) 2.2 You want it to show the display (default yes) (Y/N):''')
                sys.stdout.flush()
                choise = sys.stdin.readline().strip().upper()
                if choise in ('N','Y'):
                    break
                sys.stdout.write(colorama.Fore.RED + colorama.Style.BRIGHT +'\x1b[A' + '''(/) SELECT A VALID CHOISE'''+ " "*100 + '\r')
                sys.stdout.flush()

            sys.stdout.write(colorama.Fore.GREEN + colorama.Style.BRIGHT +'\x1b[A' + f"(-) 2.2 You want it to show the display (default yes) (Y/N): {choise}" + '\r\n')
            sys.stdout.flush()

            if choise =="Y":
                linux_function(get_path(),display=True)
                update_toml("display_console",True)
            else:
                linux_function(get_path(),display=False)
                update_toml("display_console",False)
    update_toml("first_setup",False)


def setup(launch_start,defaul_start,display_console):
    """This function is used for setting up all of the things that are needed before running the programm. It will create a config file and also check whether.

    Args:
        launch_start (bool): _description_
        defaul_start (str): _description_
        display_console (bool): _description_
    """
    while True:
        sys.stdout.write(colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT + f'''

 - CURRENT SYSTEM: [{platform.system()}]
----- [WHAT DO YOU WISH TO MODIFY] -----
'''
+
colorama.Fore.BLUE +'''
[-1 ] EXIT
[ 0 ] Display the settings
[ 1 ] Launch script at system startup?
[ 2 ] Default startup?
[ 3 ] Show diplay?

''')
        sys.stdout.flush()

        sys.stdout.write(colorama.Fore.CYAN + colorama.Style.BRIGHT + '''[ - ] Input: ''')
        sys.stdout.flush()
        choise = sys.stdin.readline().strip().upper()


        if choise == '0':
            show_settings()
        elif choise == '1':
            if platform.system() == "Windows":
                modify_start_startup_win(launch_start)
            else:
                modify_start_startup_lin(launch_start,display_console)
        elif choise == '2':
            while True:
                choise = input("You want to eliminate the possibility of a default startup (Y/N): ").upper()
                if choise in ('Y','N'):
                    break
                sys.stdout.write(colorama.Fore.RED + colorama.Style.BRIGHT +'\x1b[A' + '''(/) SELECT A VALID CHOISE'''+ " "*100 + '\r')
                sys.stdout.flush()

            if choise == 'N':
                if defaul_start == 'T':
                    update_toml("defaul_start",'R')
                else:
                    update_toml("defaul_start",'T')
            else:
                update_toml("defaul_start",'N')
            print(SUCCESS_MESSAGE,flush=True)

        elif choise == '3':
            modify_display()
        elif choise == '-1':
            return
        else:
            sys.stdout.write(colorama.Fore.RED + colorama.Style.BRIGHT +'\x1b[A' + '''(/) SELECT A VALID CHOISE'''+ " "*100 + '\r')
            sys.stdout.flush()

def get_path():
    """Get path to current dir.

    Returns:
        str: Path
    """
    current_folder = os.getcwd()
    parent_folder = os.path.dirname(current_folder)
    return parent_folder

def main():
    """Main function."""
    subprocess.run("poetry install",shell=True,check=True)

    print(colorama.Style.BRIGHT + colorama.Fore.MAGENTA +
          pyfiglet.figlet_format("  Virgil", font="doh", width=200), flush=True)

    # ------ SETUP -------
    first_setup,launch_start,defaul_start,display_console = get_data()

    parent_folder = get_path()

    system = check_system()
    if system == "N":
        print("Virgil AI is only supported in Windows and Linux.",flush=True)
        return SystemError

    cli = windows_function if system == "W" else linux_function

    print(colorama.Fore.GREEN + pyfiglet.figlet_format("WELCOME",
          justify="center", font="digital"),flush=True)
    print('''

 Welcome to''' + colorama.Fore.GREEN + colorama.Style.BRIGHT + " Virgil AI" + colorama.Fore.WHITE + ''' i remind you that AI does not stand for Aritificial Intelligence
 but for  ''' + colorama.Fore.RED + colorama.Style.BRIGHT + "Assistant Interface" + colorama.Fore.WHITE + ''' after this premise we can start with the setup
 read carefully the description and if you have doubts go here ''' + colorama.Fore.BLUE + "https://github.com/Retr0100/VirgilAI", flush=True)

    # ------- END SETUP -----

    if first_setup :
        if system == "L":
            #DOWNLOAD OFF SOME PACKET
            subprocess.run("sudo apt install python3-pyaudio;sudo apt install ffmpeg;sudo apt install screen",shell=True,check=True)
        first_start(cli,parent_folder)
    else:
        setup(launch_start,defaul_start,display_console)



if __name__ == '__main__':
    colorama.init(autoreset=True)
    main()
