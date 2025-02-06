# Google Drive Command Line Tool

## Description
This script allows interaction with Google Drive directly from the terminal. It enables listing files, uploading and downloading files, changing the download destination folder, and logging out from the account.

## Installation
1. Clone the repository or download the script to your desired folder.
2. Install the required dependencies by running:
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure you have the credentials to access Google Drive.

## Usage

### List files in a Google Drive folder
```sh
python drive.py --list-files folder
```
To display all files in your main Drive:
```sh
python drive.py --list-files root
```

### Upload a file to Google Drive
```sh
python drive.py --upload /path/to/file /path/to/destination/folder
```

### Download a file from Google Drive
```sh
python drive.py --download /path/to/file
```

### Change the download destination folder
```sh
python drive.py --change-download-destination /new/path/to/folder
```

### Logout from Google account
```sh
python drive.py --logout
```

## Running from any directory
To run the script from any directory, add its folder to the `~/.bashrc` file:
```sh
echo 'export PATH="$PATH:/path/to/folder"' >> ~/.bashrc
source ~/.bashrc
```
Now you can run the script from any location with:
```sh
drive.py --list-files root
```

