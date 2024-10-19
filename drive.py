#! /bin/python3

from os import remove
import io
import os.path
from argparse import ArgumentParser, ArgumentError, ArgumentTypeError
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from filesFunction import getFiles, printFiles, get_folder_id, get_file_id
from customErrors import *

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", 
          "https://www.googleapis.com/auth/drive"]

def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("/home/anto/code/projects/drive/token.json"):
    creds = Credentials.from_authorized_user_file("/home/anto/code/projects/drive/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "/home/anto/code/projects/drive/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("/home/anto/code/projects/drive/token.json", "w") as token:
      token.write(creds.to_json())


  parser = ArgumentParser(
    description="Command line tool to interact with google drive")

  parser.add_argument(
    "--list-files", 
    "-ls",
    metavar="folder-path",
    help="List all the files and folders in a directory (use root as folder-path to list My drive)",)
  
  parser.add_argument(
    "--upload",
    "-u",
    metavar=("file-path", "destination-folder-path"),
    help="Upload a file in a specific folder.",
    nargs=2
  )

  parser.add_argument(
    "--download",
    "-d",
    metavar="file-path",
    help="download a file from drive")
  
  parser.add_argument("--logout", action="store_true")

  try:
    service = build("drive", "v3", credentials=creds)

    args = parser.parse_args()
    page_token = None
    
    if args.logout:
      if os.path.exists("token.json"):
        remove("token.json")
        
      return
      
    if args.list_files:

      path_id = "root"
        
      #? list_files contains the path of the folder to print
      if args.list_files != "root":
        path = args.list_files.split("/")
        for folder in path:
          path_id = get_folder_id(service, folder, path_id)

      while True: 
        items, page_token = getFiles(service, page_token, path_id)

        if not items:
          print("No files found.")
          return

        print("My drive" if path_id == "root" else args.list_files)
        printFiles(items)

        if not page_token: 
          break

    if args.upload:
      if len(args.upload) < 2:
          raise ArgumentError(parser._actions[1], message="File path and destination path are both required")

      #? upload[0] contains file-path and upload[1] contains destination-path    
      path_id = "root"

      if args.upload[1] != "root":
        path = args.upload[1].split("/")
        for folder in path:
          path_id = get_folder_id(service, folder, path_id)

      file_metadata = {"name": os.path.basename(args.upload[0]),
                        "parents": [path_id]}
      
      media = MediaFileUpload(args.upload[0], resumable=True)

      service.files().create(body=file_metadata,
                            media_body=media,
                            fields="id").execute()
      
      print("Upload completed")
          
    if args.download:
      path = args.download.split("/")
      file_name = path[len(path)-1]

      file_id = get_file_id(service, file_name)

      request = service.files().get_media(fileId = file_id)
      fh = io.FileIO(f"/home/anto/Scaricati/{file_name}", 'wb')
      downloader = MediaIoBaseDownload(fh, request)

      done = False
      while not done:
          status, done = downloader.next_chunk()
          print(f"Download progress: {int(status.progress() * 100)}%")
    
  except (HttpError, ArgumentError, FolderError, NonExistentFileError) as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()