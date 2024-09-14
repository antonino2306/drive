def getFiles(service, page_token): 
  results = (
        service.files()
        .list(
          #? "root in parents" mi permette di ottenere tutte le cartelle che si trovano
          #? in "My drive"
          q = "'root' in parents",
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

