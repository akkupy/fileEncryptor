import random
import string
import os

def string_generator(size=3, string=string.ascii_letters + string.digits):    
    return ''.join(random.choice(string) for _ in range(size))

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     return True
   except OSError:
     return False

    
def count_files_in_directory(dir_path):
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count