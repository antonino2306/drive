from sys import executable
from subprocess import check_call
from configFunctions import check_dependencies
from os.path import abspath, dirname

def install_dependencies():

    code_folder = dirname(abspath(__file__))

    missing_packages = check_dependencies(code_folder)

    if missing_packages:
        print("Installazione dipendenze mancanti")
        check_call(executable, "-m", "pip", "install", *missing_packages)
        print("Tutte le dipendenze sono state installate")
    else: 
        print("Tutte le dipendenze sono già installate")


if __name__ == "__main__":
    install_dependencies()