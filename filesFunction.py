from customErrors import *

def get_folder_id(service, folder_name, parent = "root"):
  query = f"mimeType = 'application/vnd.google-apps.folder' and '{parent}' in parents and name='{folder_name}'"
  
  results = service.files().list(q=query, fields="files(id, name)").execute()

  folder = results.get("files", [])

  if not folder:
    raise FolderError(f"The folder named {folder_name} doesn't exist. Check the path")

  return folder[0]["id"]

def get_file_id(service, file_name):
   results = service.files().list(
        q=f"name='{file_name}'",
        fields="files(id, name)",
        pageSize=10
    ).execute()
   
   items = results.get("files", [])

   if not items: 
     raise NonExistentFileError(f"Can't find a file named: {file_name}")
   
   return items[0]["id"]

def getFiles(service, page_token, parent="root"): 
  
  results = (
        service.files()
        .list(
          #? "root in parents" mi permette di ottenere tutte le cartelle che si trovano
          #? in "My drive"
          
          q = f"'{parent}' in parents",
          pageSize = 10, 
          fields = "nextPageToken, files(mimeType, id, name, size)",
          orderBy = "folder, name",
          pageToken = page_token
        )
        .execute()
    )
  
  return [results.get("files", []), results.get("nextPageToken", None)]

def printFiles(items): 
  for i, item in enumerate(items):

      if item["mimeType"] == "application/vnd.google-apps.folder":
        print(f"{i}: \033[94m{item["name"]}\033[0m")
  
      else : 
        print(f"{i}: {item['name']} {item["size"]} byte")
    
      i+=1
