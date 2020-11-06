from aita.interface import main
from tqdm import tqdm
from pathlib import Path

import os
import sys
import requests

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_URL = ["https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.data-00000-of-00001",
        "https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.index",
        "https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.meta"]

def download_model():
    filesize = int(requests.head(url).headers["Content-Length"])
    filename = os.path.basename(url)
    dl_path = os.path.join(home_path, sub_path, filename)
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

if not (os.path.exists(os.path.join(SCRIPT_PATH,'model','pytorch_model.bin')) or os.path.exists(os.path.join(SCRIPT_PATH,'model','model-ckpt.index'))):
    print("AI model is not found. Should I download it?", end='')
    if input('(Y/n)').lower() == 'y':
        download_model()
    else: 
        print('Using online feature.')
        # TODO: Check internet
        print('Online feature requires subscription. Please enter your ID.')
        user_id = input('ID: ')

main()