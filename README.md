# ai-text-adventure
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fksjae%2Fai-text-adventure%2Fbadge&style=flat)](https://actions-badge.atrox.dev/ksjae/ai-text-adventure/goto)

A text adventure game example based on [custom pretrained GPT2](https://github.com/ksjae/KoGPT). 
한국어 매뉴얼은 README_KR.md를 참조해 주세요.

*This program is developed actively, and may not be stable.*

## Running this game

**WARNING : Multilingual support is WIP. Language selection may not work properly.**
Pre-requisites : Working python install
Recommended : python 3.8.5 and a nvidia graphics card(supports CUDA 10.1) with more than 6GB VRAM

1. clone this repo
2. ```python3 -m venv aita```
3. ```source aita/bin/activate```
4. ```pip install -r requirements.txt```
5. ```python3 main.py```

## Using the framework

Edit the following files at your leisure - 
- ```actions.py``` for custom action calls
- ```constants.py``` for project-wide constants (i.e. API Endpoint)
- ```customclass.py``` for python classes used in-game (i.e. characters)
- ```errors.py``` for custom error handling
- ```generator.py``` for text generation (HuggingFace transformers & [KoGPT](https://github.com/ksjae/KoGPT) compatible)
- ```interface.py``` for user interface (terminal)
- ```utils.py``` for utility functions (i.e. custom sort)

## LICENSE

Any use of resources in this repository is possible, as long as it's for non-commercial purposes.
This does not override other licenses set to parts of this repository such as corpora or initial story generator contents.

### LICENSES by parts
[The Korean GPT2](https://github.com/ksjae/KoGPT): Public Domain
[Initial Story Generator(EN)](https://blog.reedsy.com): Non-commercial
Initial Story Generator (Korean Translation): Non-commercial, Attribution
