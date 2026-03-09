import streamlit as st
import pandas as pd

df = pd.DataFrame({"Value": [1000, 20000, 300000]})
st.dataframe(df, column_config={"Value": st.column_config.NumberColumn(format="%d")})
st.dataframe(df, column_config={"Value": st.column_config.NumberColumn(format="%,d")})
st.dataframe(df, column_config={"Value": st.column_config.NumberColumn(format="%f")})
st.dataframe(df.style.format("{:,}"))
