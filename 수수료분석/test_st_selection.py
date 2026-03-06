import streamlit as st
import pandas as pd

df = pd.DataFrame({'제휴사명': ['삼성생명', '농협생명'], '금액': [1000, 2000]})
try:
    event = st.dataframe(df, selection_mode='single-row', on_select='rerun')
    st.write("Selection works:", event.selection.rows)
except Exception as e:
    st.write("Selection failed:", str(e))
