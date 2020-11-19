import os
# PATH
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
DATA_PATH = os.path.join(SCRIPT_PATH,'data')

# URLs
MODEL_URL_KO = ["https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.data-00000-of-00001",
        "https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.index",
        "https://static.ksjit.com/KoGPT-v0.2.1/xl/model.ckpt-800000.meta"]
MODEL_URL_EN = ["https://cdn.huggingface.co/gpt2-xl-pytorch_model.bin"]
API_ENDPOINT = "https://static.ksjit.com/"
AUTH_ENDPOINT = "https://static.ksjit.com/"

# KEY CODES
CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 
KEY_DOWN = '\x1b[B'
KEY_UP = '\x1b[A'

# TEXTs
MOVE_MODE = "이동"
FIGHT_MODE = "전투"
TALK_MODE = "대화"
YES = '네'
NO = '아니오'