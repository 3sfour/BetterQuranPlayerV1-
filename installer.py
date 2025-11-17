import os
import zipfile
import shutil
import hashlib

import requests

from config import INSTALL_PATH

class QuranInstaller:
    """This class handles the installing formatting hash verification and organizing of the audio obtained from the zip file."""

    def __init__(self, reciter):
        self.reciter = reciter
        self.output_path = INSTALL_PATH

    def download(self):
        """Downloads zips based off of the selected reciter"""


        # Choosing reciter to download
        match self.reciter:
            case "Abdul_Basit_Mujawwad":
                url = "https://everyayah.com/data/Abdul_Basit_Mujawwad_128kbps/000_versebyverse.zip"
       
            case "Abdul_Basit_Murratal":
                url= "https://everyayah.com/data/Abdul_Basit_Murattal_192kbps/000_versebyverse.zip"

            case "Husary_Mualim":
                url = "https://everyayah.com/data/Husary_Muallim_128kbps/000_versebyverse.zip"

            case "Al-Alafasy":
                url = "https://everyayah.com/data/Alafasy_64kbps/000_versebyverse.zip"
            case _:
                raise ValueError(f"Invalid reciter: {self.reciter}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        zip_path = os.path.join(self.output_path,"audio.zip")
        with open(zip_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def extract(self):
        """Extracts the downloaded zip"""

        with zipfile.ZipFile(os.path.join(self.output_path, "audio.zip"),"r") as zip_ref:
            zip_ref.extractall(self.output_path)

    def check_hash(self):
        """Checks hashes based off of the hash file that is given after extracting the zip file."""

        check_sum = os.path.join(self.output_path,"000_checksum.md5")
        with open(check_sum,"r") as file:
            hashes = []
            for line in file:
                line =  line.split()
                file_hash = line[0]
                hashes.append(file_hash)
        gen_hashes = []
        for filename in os.listdir(self.output_path):
            file_path = os.path.join(self.output_path,filename)
            if not filename.lower().endswith(".mp3"):
                continue
            # If os.path.isfile(file_path):
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
            generated_hash = md5_hash.hexdigest()
            gen_hashes.append(generated_hash)
            
        return(gen_hashes == hashes)

    def rename(self):      
        """Renames each file into the chapter|verse.mp3 format."""

        directory_path = self.output_path

        for filename in os.listdir(directory_path):
            if not filename.lower().endswith(".mp3"):
                continue

            chapter_number = filename[:3]
            verse_number = int(filename[3:-4])
            new_filename = f"{int(chapter_number)}|{int(verse_number)}.mp3"
            
            oldpath = os.path.join(directory_path,filename)
            newpath = os.path.join(directory_path,new_filename)

            os.rename(oldpath,newpath) 

    def organize(self):
        """Organize each file into its own folder based on the chapter name."""

        directory_path = self.output_path
        new_folders = []

        for filename in os.listdir(directory_path): # This is finding all of the names 
            chapter_number = ""
            if not filename.lower().endswith(".mp3"):
                continue
            for char in filename:
                if char != "|":                 # This is finding the  number of the chpater
                    chapter_number += char
                else:
                    break
            

            chapter_number = int(chapter_number)    # Makes it a int so it can be used ot make folders

            if chapter_number not in new_folders:   # If the chpater isnt included add it
                new_folders.append(chapter_number)
        print(new_folders)

        # This is going to make all of the folders for each name in the list
        for chapter_number in new_folders:
            os.makedirs(f"{directory_path}/{chapter_number}",exist_ok=True) # Exist to prevent erros if the folder is already there

        for filename in os.listdir(directory_path): # This is finding all of the names 
            chapter_number = ""
            dirs = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path,d))]
            for char in filename:
                if char != "|":                 # This is finding the  number of the chpater
                    chapter_number += char
                else:
                    break
            for d in dirs:
                if d == chapter_number:
                    shutil.move(os.path.join(directory_path, filename), os.path.join(directory_path, d))   
    def run(self):
        """Downloads zip extracts it checks the hash renames all of the files and organizes them into folders based on the chapters they belong too."""

        self.download()
        self.extract()
        if self.check_hash():
            print("Hashing Passed")
            self.rename()
            self.organize()
        else:
            print("some hashes didn't match")
            
        
        
        
        