from flask import Flask, request, send_file
import os
import shutil
import subprocess
import uuid
import threading

from lib.models.upscaling_order import UpscalingOrder
from lib.models.upscaling_queue import UpscalingQueue

threading.Thread(target=UpscalingQueue.manage_upscaling).start()

TEMP_INPUT_DIR = "./temp_input_dir"  # Temporary directory for holding the image to be sent
app = Flask(__name__)

os.makedirs(r"results\HAT_GAN_Real_SRx4\visualization\custom", exist_ok=True)

@app.route('/upscale', methods=['POST'])
def upscale_image():
    print("Received request")
    # Check if the post request has the file part
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    
    # If the user does not select a file
    if file.filename == '':
        return "No selected file", 400
    
    print(file.filename)

    # Save the file to the input directory
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(TEMP_INPUT_DIR, f'{unique_id}{file.filename}')
    file.save(input_path)
    print("Saved file to", input_path)
    order = UpscalingOrder(unique_id, input_path)
    UpscalingQueue.put(order)
    
    
    # Wait for the output file to be created
    output_dir = None
    while output_dir is None:
        output_order = UpscalingQueue.output_queue.get()
        if output_order.unique_id == unique_id:
            print("Found output file")
            output_dir = output_order.output_file_path
        else:
            UpscalingQueue.output_queue.put(output_order)
    # Send the copied upscaled image back to the user
    response = send_file(output_dir, as_attachment=True)
    return response

if __name__ == '__main__':
    app.run(debug=True)
