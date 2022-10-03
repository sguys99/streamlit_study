# https://www.youtube.com/watch?v=TXSOitGoINE
# https://gist.github.com/Sven-Bo/31d98f80b5fed1d3f53cf98e5b61e7c9
# https://github.com/andfanilo/streamlit-lottie


import json

import requests  # pip install requests
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

# GitHub: https://github.com/andfanilo/streamlit-lottie
# Lottie Files: https://lottiefiles.com/

def load_lottiefile(filepath: str): # 저장된 json 파일 읽는 방식
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str): # url 읽어오는 방식
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.title('Include Lottie Files in Streamlit')

lottie_coding = load_lottiefile("lottiefile.json")  # replace link to local lottie file
lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")

st_lottie(lottie_coding,
          speed = 1,
          reverse=False,
          loop=True,
          quality='low',
          height=100,
          width=100)

# st_lottie(
#     lottie_hello,
#     speed=1,
#     reverse=False,
#     loop=True,
#     quality="low", # medium ; high
#     renderer="svg", # canvas
#     height=None,
#     width=None,
#     key=None,
# )