import streamlit as st

def metric_card(title, value):

    with st.container(border=True):
        st.metric(
            label=title,
            value=value
        )