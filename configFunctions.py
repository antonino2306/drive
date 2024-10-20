import os

def configure_destination_folder():
    if os.path.exists("/home/anto/code/projects/drive/config.txt"):
        with open("/home/anto/code/projects/drive/config.txt") as config_file:
            return config_file.readline()
        
    else:
        print("""Inserisci il percorso della cartella in cui vuoi memorizzare i file scaricati.
              Esempio: /home/username/Scaricati""")
        destination_path = input("> ")
        with open("/home/anto/code/projects/drive/config.txt", "w") as config_file:
            config_file.write(destination_path)
        
        return destination_path
    

def change_destination_folder(path):
    with open("/home/anto/code/projects/drive/config.txt", "w") as config_file:
        config_file.write(path)

    print("Cartella di destinazione cambiata con successo")
