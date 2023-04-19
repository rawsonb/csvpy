import os
import time

def delete_old_files(folder_path, file_age_days):
    for filename in os.listdir(folder_path):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_age_secs = time.time() - os.path.getmtime(file_path)
            print(file_age_secs)
            if file_age_secs > file_age_days * 86400:
                os.remove(file_path)