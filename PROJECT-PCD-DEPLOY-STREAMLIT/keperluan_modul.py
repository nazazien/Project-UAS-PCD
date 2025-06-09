import streamlit as st
import os
import time
import base64
from datetime import datetime
from math import ceil
import csv
import pemanis
import cv2
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

def gambar(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def bg():
    img1 = gambar("Documents/image/a.png")
    img2 = gambar("Documents/image/b.png")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url(data:image/jpeg;base64,{img1});
        background-size: cover;
        background-position: center;
    }}
    [data-testid="stSidebar"] {{
        background-image: url("data:image/png;base64,{img2}");
        background-size: cover;
        background-position: center;
    }}
    [data-testid="stAppHeader"], [data-testid="stHeader"], [data-testid="stAppHeader"] *, [data-testid="stHeader"] * {{
        background-color: rgba(0, 0, 0, 0) !important;
        backdrop-filter: none !important;
    }}
    .st-emotion-cache-12fmjuu, .st-emotion-cache-15ecox0,
    .st-emotion-cache-1p1m4ay, .st-emotion-cache-1dp5vir {{
        background-color: rgba(0, 0, 0, 0) !important;
    }}
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
