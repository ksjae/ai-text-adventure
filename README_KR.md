# ai-text-adventure
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fksjae%2Fai-text-adventure%2Fbadge&style=flat)](https://actions-badge.atrox.dev/ksjae/ai-text-adventure/goto)

[한국어 GPT2](https://github.com/ksjae/KoGPT) 기반 텍스트 어드벤쳐 게임입니다. 

*현재 개발 중이며, 프로그램의 기능은 상시로 변경될 수 있습니다.*

## 게임 실행법

**경고 : 다국어 선택 옵션은 현재 개발 중입니다. 정상 작동을 보증하지 않습니다.**

필수: Python

권장: python 3.8.5, CUDA 10.1지원 그래픽카드(엔비디아 그래픽카드, 6GB 이상 VRAM)

1. 이 저장소 복제
2. ```python3 -m venv aita```
3. ```source aita/bin/activate```
4. ```pip install -r requirements.txt```
5. (macOS 11.0+ 이상만 해당) [여기](https://github.com/apple/tensorflow_macos/releases)서 tensorflow를 설치하세요 (더 빠릅니다).
5. ```python3 main.py```

## 프레임워크 이용하기

본 게임은 프레임워크 위에서 AI 모델을 활용하고 있습니다. 프레임워크만 따와서 다른 게임을 만들 수도 있습니다.

아래 파일을 알맞게 수정하시면 됩니다 - 
- ```actions.py``` for custom action calls
- ```constants.py``` for project-wide constants (i.e. API Endpoint)
- ```customclass.py``` for python classes used in-game (i.e. characters)
- ```errors.py``` for custom error handling
- ```generator.py``` for text generation (HuggingFace transformers & [KoGPT](https://github.com/ksjae/KoGPT) compatible)
- ```interface.py``` for user interface (terminal)
- ```utils.py``` for utility functions (i.e. custom sort)

## LICENSE

아래 따로 지정되지 않은 코드의 경우 저자 공개 의무가 없는 비영리 이용을 원칙으로 합니다.
다른 라이선스가 필요하시면 issue 올려주시면 제가 알맞게 수정하겠습니다.

### LICENSES by parts
[The Korean GPT2](https://github.com/ksjae/KoGPT): 공개
[Initial Story Generator(EN)](https://blog.reedsy.com): 비영리
Initial Story Generator (번역본): 비영리, 저자 공개 의무
