# its going to go like for chapter name if chapter name is not in the list add it 
# after that you are going to make a directory for each name in the list corresponding to the name
# after that you are going to go through all of the file names one more time and if the chpater name corresponds to a directory put it in that directory
import os
import shutil


directory_path = (f"{os.getcwd()}/audio")
new_folders = []

for filename in os.listdir(directory_path): # this is finding all of the names 
    chapter_number = ""
    for char in filename:
        if char != "|":                 # this is finding the  number of the chpater
            chapter_number += char
        else:
                break
    

    chapter_number = int(chapter_number)    # makes it a int so it can be used ot make folders

    if chapter_number not in new_folders:   # if the chpater isnt included add it
        new_folders.append(chapter_number)
    else:
        pass
print(new_folders)

# # this is going to make all of the folders for each name in the list
for chapter_number in new_folders:
     os.makedirs(f"{directory_path}/{chapter_number}",exist_ok=True) # exist to prevent erros if the folder is already there

# files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

# print(files)


for filename in os.listdir(directory_path): # this is finding all of the names 
    chapter_number = ""
    dirs = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path,d))]
    for char in filename:
        if char != "|":                 # this is finding the  number of the chpater
            chapter_number += char
        else:
            break
    for d in dirs:
        if d == chapter_number:
            shutil.move(os.path.join(directory_path, filename), os.path.join(directory_path, d))

    
