import streamlit as st

st.set_page_config(page_title="Placement App", page_icon="🎓")

# st.sidebar.markdown("## 🎓 Placement App")
# st.sidebar.markdown("---")

insight_page = st.Page("insight.py", title="Insight",icon="📊")
filter_page = st.Page("filter.py", title="Filter",icon="🔍")

pg = st.navigation([insight_page, filter_page])
st.markdown("# 🎓 Placement Eligibility App")
pg.run()