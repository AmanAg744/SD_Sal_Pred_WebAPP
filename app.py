import streamlit as st
from predict_page import show_prediction
from explore_page import show_explorations

page = st.sidebar.selectbox("Explore or Predict",("Explore","Predict"))
if page == "Explore":
    show_explorations()
else:
    show_prediction()
    