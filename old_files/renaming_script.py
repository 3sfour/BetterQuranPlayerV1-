import os
directory_path = (f"{os.getcwd()}/audio")

for filename in os.listdir(directory_path):
    chapter_number = filename[:3]
    verse_number = int(filename[3:-4])
    new_filename = f"{int(chapter_number)}|{int(verse_number)}.mp3"
    
    oldpath = os.path.join(directory_path,filename)
    newpath = os.path.join(directory_path,new_filename)

    os.rename(oldpath,newpath) 