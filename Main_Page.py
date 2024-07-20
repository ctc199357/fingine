import streamlit as st
import time

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.markdown("### Hi Ken!  Welcome to FinGenie! 🧞")

_LOREM_IPSUM =   """
#### To know about your expense and spending habits immediately, just do the following!
1. Upload any **receipts image, bank statements or spending-related documents**
"""

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.07)

st.write_stream(stream_data)