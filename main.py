from aita.interface import main
from aita.customclass import *
from aita.constants import *
from tqdm import tqdm
from pathlib import Path

import os
import sys
import time
import requests

flags = AppFlags()
flags.is_dev = True

def download_model():
    filesize = int(requests.head(url).headers["Content-Length"])
    filename = os.path.basename(url)
    dl_path = os.path.join(SCRIPT_PATH, 'model', filename)
    chunk_size = 1024
    with requests.get(url, stream=True) as r, open(dl_path, "wb") as f, tqdm(
        unit="B",  # unit string to be displayed.
        unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
        unit_divisor=1024,  # is used when unit_scale is true
        total=filesize,  # the total iteration.
        file=sys.stdout,  # default goes to stderr, this is the display on console.
        desc=filename  # prefix to be displayed on progress bar.
        ) as progress:
            for chunk in r.iter_content(chunk_size=chunk_size):
                # download the file chunk by chunk
                datasize = f.write(chunk)
                # on each chunk update the progress bar.
                progress.update(datasize)

if os.path.exists(os.path.join(SCRIPT_PATH,'model','pytorch_model.bin')):
    flags.model_path = os.path.join(SCRIPT_PATH,'model')
    flags.model_type = 'torch'
elif os.path.exists(os.path.join(SCRIPT_PATH,'model','model-ckpt-800000.index')):
    flags.model_path = os.path.join(SCRIPT_PATH,'model')
    flags.model_type = 'tf'
else:
    print("AI model is not found. Download it?", end='')
    if input('(Y/n)').lower() == 'y':
        download_model()
    else: 
        print('Using online feature.')
        # TODO: Check internet
        print('Online feature requires subscription. Please enter your ID.')
        
        ## AUTH ##
        user_id = input('ID: ')
        while True:
            response = requests.get(f"{AUTH_ENDPOINT}/{user_id}")
            if response.status_code != 200:
                print('Wrong ID :(')
                time.sleep(1)
                user_id = input('ID: ')
            else:
                break
        flags.user_id = user_id
            

main(flags)