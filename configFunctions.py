import os
from json import load, dump

def first_configuration(code_folder):
    default_download_path = f"{os.path.expanduser("~")}/drive_downloads"
    os.mkdir(default_download_path)
    with open(f"{code_folder}/config.json", "w") as config_file:
        config = {
            "base_folder": os.path.expanduser("~"),
            "download_folder": default_download_path
        }
        dump(config, config_file, indent=4)



# def configure_destination_folder():
#     if os.path.exists("/home/anto/code/projects/drive/config.txt"):
#         with open("/home/anto/code/projects/drive/config.txt") as config_file:
#             return config_file.readline()
        
#     else:
#         print("""Inserisci il percorso della cartella in cui vuoi memorizzare i file scaricati.
#               Esempio: /home/username/Scaricati""")
#         destination_path = input("> ")
#         with open("/home/anto/code/projects/drive/config.txt", "w") as config_file:
#             config_file.write(destination_path)
        
#         return destination_path
    

def change_destination_folder(code_folder, path):

    with open(f"{code_folder}/config.json", "r") as config_file:
        config = load(config_file)

    with open(f"{code_folder}/config.json", "w") as config_file:
        config["download_folder"] = path
        dump(config, config_file, indent=4)
         
    print("Cartella di destinazione cambiata con successo")
