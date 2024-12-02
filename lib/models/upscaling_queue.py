from queue import Queue
import queue
from lib.models.upscaling_order import UpscalingOrder

class UpscalingQueue:
    OUTPUT_DIR = "output_dir"
    
    input_queue = Queue()
    output_queue = Queue()
    
    
    
    @staticmethod
    def put(order:UpscalingOrder):
        UpscalingQueue.queue.put(order)
        
    @staticmethod
    def manage_upscaling():
        while True:
            order = UpscalingQueue.input_queue.get()
            order.upscale_and_save(UpscalingQueue.OUTPUT_DIR)
            UpscalingQueue.output_queue.put(order)
            
    @staticmethod
    def put(order:UpscalingOrder):
        UpscalingQueue.input_queue.put(order)
            
        
        
        
    
