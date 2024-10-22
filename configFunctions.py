import os
from json import load, dump
import pkg_resources
from sys import executable
from subprocess import check_call

def check_dependencies(code_folder):
    with open(f"{code_folder}/requirements.txt", "r") as dependencies_list:
        dependencies = dependencies_list.read().splitlines()
        
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]

    missing_packages = []
    for pkg in dependencies:
        pkg_name = pkg.split("==")[0]
        if pkg_name not in installed_packages:
            missing_packages.append(pkg_name)

    return missing_packages

def install_dependencies(missing_packages):

    print("Installazione dipendenze mancanti")
    check_call(executable, "-m", "pip", "install", *missing_packages)

    print("Tutte le dipendenze sono state installate")
    
def first_configuration(code_folder):

    missing_packages = check_dependencies(code_folder)
    if missing_packages:
        install_dependencies(missing_packages)

    default_download_path = f"{os.path.expanduser("~")}/drive_downloads"
    os.mkdir(default_download_path)
    with open(f"{code_folder}/config.json", "w") as config_file:
        config = {
            "base_folder": os.path.expanduser("~"),
            "download_folder": default_download_path
        }
        dump(config, config_file, indent=4)
    

def change_destination_folder(code_folder, path):

    with open(f"{code_folder}/config.json", "r") as config_file:
        config = load(config_file)

    with open(f"{code_folder}/config.json", "w") as config_file:
        config["download_folder"] = path
        dump(config, config_file, indent=4)
         
    print("Cartella di destinazione cambiata con successo")

