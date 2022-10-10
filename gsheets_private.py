# https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers = 1)
    rows = rows.fetchall()
    return rows


sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

df = pd.DataFrame(rows)
st.dataframe(df)

# for row in rows:
#     st.write(f"{row.begin_dtm}, {row.end_dtm}, {row.food_id}, {row.food_name}, {row.amount}, \
#               {row.carb}, {row.fat}, {row.protein}, {row.calories}")

