from aita.interface import main
from aita.customclass import *
from aita.constants import *
from aita.generator import *
from tqdm import tqdm

import os
import sys
import requests

flags = AppFlags()
flags.is_dev = False
flags.use_generator = True

def download_model(url):
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


def checkInternetRequests(url='http://www.google.com/', timeout=3):
    '''
    Checks for internet connectivity
    source: https://medium.com/better-programming/how-to-check-the-users-internet-connection-in-python-224e32d870c8
    '''
    try:
        requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError as ex:
        return False

generator = Generator()

if not flags.is_dev:
    flags.LANG = input('Which language should be used? (en/ko) : ')
    NO_MODEL = True
    if flags.LANG == 'ko':
        flags.model_path = os.path.join(SCRIPT_PATH,'model','ko')
        if os.path.exists(os.path.join(SCRIPT_PATH,'model','ko','pytorch_model.bin')):
            flags.model_type = 'pt'
            NO_MODEL = False
        elif os.path.exists(os.path.join(SCRIPT_PATH,'model','ko','model-ckpt-800000.index')):
            flags.model_type = 'tf'
            NO_MODEL = False

    elif flags.LANG == 'en':
        flags.model_type = 'pt'
        flags.model_path = 'gpt2'
        NO_MODEL = False

    if NO_MODEL:
        print("AI model is not found. Download it?", end='')
        if input('(Y/n)').lower() == 'y':
            for url in MODEL_URL[flags.LANG]:
                download_model(url)
        else: 
            print('Using online feature.')
            if checkInternetRequests() is False:
                print("INTERNET REQUIRED. Please check internet connectivity or change back to local mode.")
                quit()

    print('LOADING...')
    
    if flags.model_type == 'pt':
        generator = HFGenerator(flags, flags.model_path)


main(flags, generator)