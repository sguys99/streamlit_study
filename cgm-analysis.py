import streamlit as st
import pandas as pd
import datetime
###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
###################################
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from functionforDownloadButtons import download_button
st.set_page_config(layout="wide")
st.header("""Simple CGM data analysis app""")
st.markdown('-----------------------------------------------------')
st.markdown("Welcome to Simple CGM data analysis app. \
            For more information, please visit our [repository](https://github.com/givita-ai)!")

c29, c30, c31 = st.columns([1, 6, 1])

with c30:

    uploaded_file = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

    if uploaded_file is not None:
        file_container = st.expander("업로드한 파일이 맞는지 확인하세요.")
        shows = pd.read_csv(uploaded_file, encoding='CP949')
        uploaded_file.seek(0)
        file_container.write(shows)

    else:
        st.info(
            # f"""
            #     👆 Upload a .csv file first. Sample to try: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
            #     """
            f"""
            👆 csv 파일을 업로드 하세요.
            """
        )

        st.stop()

from st_aggrid import GridUpdateMode, DataReturnMode

gb = GridOptionsBuilder.from_dataframe(shows)
# enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
gridOptions = gb.build()

st.success(
    f"""
        💡 Tip! shift 키를 누른 상태에서 열(row)을 클릭하면, 여러 개의 열을 선택할 수 있습니다!
        """
)

response = AgGrid(
    shows,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
)

df = pd.DataFrame(response["selected_rows"])

shows['timestamp'] = pd.to_datetime(shows['timestamp'])
date_min = shows['timestamp'].min().date()
date_max = shows['timestamp'].max().date()

st.write(f"""**데이터 수집기간** : {date_min} ~ {date_max}""")

# fig = px.line(shows, x = 'timestamp', y='glucose', title = 'Overall Glucose Trend', height=500, width=1200)
# fig.add_hline(y = 180, row=1, col=1)
# fig.add_hline(y = 70, row=1, col=1)

#st.plotly_chart(fig)

fig = make_subplots(rows=3, cols=1, vertical_spacing=0.05)
fig.update_layout(height = 800, width = 1000, title = 'Overall trend')
fig.add_trace((go.Scatter(x=shows['timestamp'], y=shows['glucose'], name='glucose')),
              row=1, col=1)
fig.add_trace((go.Scatter(x=shows['timestamp'], y=shows['meal'], name='meal')),
              row=2, col=1)
fig.add_trace((go.Scatter(x=shows['timestamp'], y=shows['activity'], name='activity')),
              row=3, col=1)

st.plotly_chart(fig)

selected_date = st.sidebar.date_input("날짜를 선택하세요.", date_min)
st.write(selected_date)

if selected_date > date_max:
    st.exception("DateError('해당 날짜의 데이터가 없습니다.')")

else:
    df_selected = shows.copy()
    df_selected['datetime'] = df_selected['timestamp'].dt.date
    df_selected = df_selected[df_selected['datetime']==selected_date]
    st.dataframe(df_selected)

    fig2 = make_subplots(rows=3, cols=1, vertical_spacing=0.05)
    fig2.update_layout(height=800, width=1000, title='특정 기간의 트렌드')
    fig2.add_trace((go.Scatter(x=df_selected['timestamp'], y=df_selected['glucose'], name='glucose')),
                  row=1, col=1)
    fig2.add_trace((go.Scatter(x=df_selected['timestamp'], y=df_selected['meal'], name='meal')),
                  row=2, col=1)
    fig2.add_trace((go.Scatter(x=df_selected['timestamp'], y=df_selected['activity'], name='activity')),
                  row=3, col=1)
    st.plotly_chart(fig2)