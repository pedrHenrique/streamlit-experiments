import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Lendo CSV
data_df = pd.read_csv(os.path.join("Data/Data.csv"))

def streamlit_interface():
    st.write(''' ## Web Visualization of Sonarqube Data ''')

if __name__ == '__main__':
    streamlit_interface()    