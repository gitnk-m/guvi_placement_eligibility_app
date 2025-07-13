import streamlit as st

insight_page = st.Page(
    "insight.py", title="Insight",
    icon="📊")

filter_page = st.Page(
    "filter.py", title="Filter",
    icon="🔍")

pg = st.navigation([insight_page, filter_page])
st.set_page_config(
    page_title="Placement App",)
st.title("Placement App")
pg.run()