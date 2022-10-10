# https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet#add-the-sheets-url-to-your-local-app-secrets

import streamlit as st
from gsheetsdb import connect

conn = connect()

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers = 1)
    rows = rows.fetchall()
    return rows


sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

for row in rows:
    st.write(f"{row.begin_dtm}, {row.end_dtm}, {row.food_id}, {row.food_name}, {row.amount}, \
              {row.carb}, {row.fat}, {row.protein}, {row.calories}")