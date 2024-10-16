import os.path

from argparse import ArgumentParser, ArgumentError, ArgumentTypeError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from filesFunction import getFiles, printFiles, get_folder_id

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", 
          "https://www.googleapis.com/auth/drive"]

def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())


  parser = ArgumentParser(
    description="Command line tool to interact with google drive")

  parser.add_argument("-execute", "-e",
                      choices = ["list-files", "upload", "download"], 
                      help = "List of all files and folder in your drive")
  
  parser.add_argument("--file-path", "-fp", help="Percorso del file")
  parser.add_argument("--destination-path", "-dp", help="Percorso di destinazione")


  try:
    service = build("drive", "v3", credentials=creds)

    args = parser.parse_args()
    page_token = None
    
    
    match args.execute: 
      case "list-files":
        while True: 
          items, page_token = getFiles(service, page_token)

          if not items:
            print("No files found.")
            return

          print("My drive:")
          printFiles(items)

          if not page_token: 
            break
        
          print("Premi s per passare alla pagina successiva")
          input()
      
      case "upload":
        if args.file_path == None:
          raise ArgumentError(parser._actions[1], message="To upload a file is required his path")
    
        if args.destination_path == None:
            raise ArgumentError(parser._actions[1], message = "Destination path is required")
        
        path = args.destination_path.split("/")
        path_ids = []
        for i in range(len(path)):
          if i == 0:
            path_ids.append(get_folder_id(service, path[i]))
          else:
            path_ids.append(get_folder_id(service, path[i], path_ids[i-1]))

        file_metadata = {"name": os.path.basename(args.file_path),
                         "parents": [path_ids[len(path_ids)-1]]}
        
        media = MediaFileUpload(args.file_path, resumable=True)

        service.files().create(body=file_metadata,
                              media_body=media,
                              fields="id").execute()
        
        print("Upload completed")
          
      case "download":
        path = args.destination_path.split("/")
        path_ids = []
        for i in range(len(path)):
          if i == 0:
            path_ids.append(get_folder_id(service, path[i]))
          else:
            path_ids.append(get_folder_id(service, path[i], path_ids[i-1]))

        print(path_ids)


      case _:
        return 
  
  except (HttpError, ArgumentError) as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()