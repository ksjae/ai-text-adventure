import os
from aita.customclass import Head, Torso, Arm, Leg, Anatomy
# PATH
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
DATA_PATH = os.path.join(SCRIPT_PATH,'data')

# URLs
MODEL_URL = {
        'ko': ["https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.data-00000-of-00001","https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.index","https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.meta"],
        }
MODEL_URL_EN = ["https://cdn.huggingface.co/gpt2-xl-pytorch_model.bin"]
API_ENDPOINT = "https://static.ksjit.com/"
AUTH_ENDPOINT = "https://static.ksjit.com/"

# KEY CODES
CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
KEY_DOWN = '\x1b[B'
KEY_UP = '\x1b[A'

# Variables
ANATOMY = Anatomy(head=Head(),
                torso=Torso(),
                arm=Arm(),
                leg=Leg(),)