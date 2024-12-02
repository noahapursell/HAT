import os
import shutil

class FileUtil:
    
    @staticmethod
    def remove_files_in_dir(dir_path:str):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                
    @staticmethod
    def copy_file(src:str, dst:str):
        shutil.copy(src, dst)