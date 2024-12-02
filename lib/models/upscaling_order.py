from lib.util.file_util import FileUtil
from dataclasses import dataclass
import subprocess
import os

@dataclass
class UpscalingOrder:
    """Class to manage an order for an image upscaling process
    """
    INPUT_DIR = "./input_dir"
    OUTPUT_DIR = "results/HAT_GAN_Real_SRx4/visualization/custom"
    TEMP_OUTPUT_DIR = "./temp_output_dir"  # Temporary directory for holding the image to be sent
    SCRIPT_COMMAND = "python hat/test.py -opt options/test/HAT_GAN_Real_SRx4.yml"
    
    unique_id:str
    input_path:str
    
    def upscale_and_save(self, output_dir:str):
        self.clean_upscaling_directories()
        FileUtil.copy_file(self.input_path, self.INPUT_DIR)
        subprocess.run(self.SCRIPT_COMMAND, shell=True)
        output_file_path = os.path.join(output_dir, f'{self.unique_id}.png')
        FileUtil.copy_file(self.find_output_file(), output_file_path)
        self.output_file_path = output_file_path
        

        
    def clean_upscaling_directories(self):
        FileUtil.remove_files_in_dir(self.INPUT_DIR)
        FileUtil.remove_files_in_dir(self.OUTPUT_DIR)
        
    def find_output_file(self):
        for f in os.listdir(self.OUTPUT_DIR):
            if f.endswith(".png") or f.endswith(".jpg"):
                output_file_path = os.path.join(self.OUTPUT_DIR, f)
                return output_file_path
            
