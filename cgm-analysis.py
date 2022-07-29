import streamlit as st
import pandas as pd
from PIL import Image
import datetime
###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode
from st_aggrid.shared import JsCode
###################################
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from functionforDownloadButtons import download_button

st.set_page_config(page_title='CGM App', page_icon=Image.open('files/givita-favicon.jpg'), layout="wide")

with open('style.css') as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

@st.cache
def get_profile_pic():
    return Image.open('files/givita-logo.jpg')

# @st.cache
# def get_data(path):
#     return pd.read_csv(path, encoding='CP949')

st.markdown("<h3 style='text-align: center; color: black;'>Simple CGM Data Analysis </h2>", unsafe_allow_html=True)
st.markdown('-----------------------------------------------------')
st.markdown("Welcome to Simple CGM data analysis app. \
            For more information, please visit our [repository](https://github.com/givita-ai)!")

logo_img = get_profile_pic()
st.sidebar.image(logo_img, use_column_width=False, width=120)
st.sidebar.header("Welcome!")


c29, c30, c31 = st.columns([1, 10, 1])

with c30:

    uploaded_file = st.file_uploader(
        "",
        key="1",
        help="넓은 화면으로 보려면 menu > Settings > wide mode 항목을 체크하세요.",
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
            👆 가지고 있는 CGM 데이터(csv 포맷)를 업로드 하세요.
            """
        )

        st.stop()


gb = GridOptionsBuilder.from_dataframe(shows)
# enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
gridOptions = gb.build()

st.success(
    f"""
        💡 Tip!  shift 키를 누른 상태에서 열(row)을 클릭하면, 여러 개의 열을 선택할 수 있습니다!
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

# df = pd.DataFrame(response["selected_rows"])

shows['timestamp'] = pd.to_datetime(shows['timestamp'])
date_min = shows['timestamp'].min().date()
date_max = shows['timestamp'].max().date()

st.write(f"""**- 데이터 크기** : {shows.shape}""")
st.write(f"""**- 수집 기간** : {date_min} ~ {date_max}""")
st.write(f"""**- 전체 차트**""")

fig1 = make_subplots(rows=3, cols=1, vertical_spacing=0.08, horizontal_spacing=0.00)
fig1.update_layout(height = 600, width = 900, margin=dict(l=0, r=0, t=10, b=0))

fig1.add_trace((go.Scatter(x=shows['timestamp'], y=shows['glucose'], name='glucose',
                          hovertext=shows['menu'],
                          hovertemplate="datetime : %{x}<br>" + "glucose : %{y}<br>" + "meal : %{hovertext}<br>",
                          line=dict(color = px.colors.qualitative.G10[0], width = 1.2))), row=1, col=1)
fig1.add_trace((go.Scatter(x=shows['timestamp'], y=shows['meal'], name='meal',
                           hovertext=shows['menu'],
                           hovertemplate="datetime : %{x}<br>" + "meal : %{hovertext}<br>",
                           line=dict(color = px.colors.qualitative.G10[1], width = 1.2))), row=2, col=1)
fig1.add_trace((go.Scatter(x=shows['timestamp'], y=shows['activity'], name='activity',
                           hovertext=shows['act_type'],
                           hovertemplate="datetime : %{x}<br>" + "activity : %{hovertext}<br>",
                           line=dict(color = px.colors.qualitative.G10[2],width = 1.2))), row=3, col=1)

st.plotly_chart(fig1, use_container_width=True)

st.sidebar.markdown(' ')
st.sidebar.markdown('*날짜 별 분석을 위해 항목을 설정하세요.*')

st.sidebar.markdown(' ')
selected_date = st.sidebar.date_input(f'날짜 선택 : {date_min} ~ {date_max}', date_min)

st.markdown(' ')
st.write(f'선택한 날짜 : {selected_date}')

default_cols = ['glucose', 'meal', 'activity']
selection_list = ['glucose', 'meal', 'activity', 'alcohol', 'meal_intensity', 'act_intensity', 'alcohol_intensity',
                  'STEP_CNT', 'MOVE_DIST', 'CNPT_CALR', 'MOVE_SPEED', 'sleep_stat']

st.sidebar.markdown(' ')
selected_cols = st.sidebar.multiselect('차트 항목', selection_list, default=default_cols)

st.sidebar.markdown(' ')
TIR_range = st.sidebar.slider("TIR 설정", 50, 200, (70, 180))

if (selected_date > date_max) | (selected_date < date_min) :
    st.exception("DateError('해당 날짜의 데이터가 없습니다.')")

else:
    df_selected = shows.copy()
    df_selected['datetime'] = df_selected['timestamp'].dt.date
    df_selected = df_selected[df_selected['datetime'] == selected_date]

    show_df = st.checkbox("데이터 표시")
    if show_df:
        st.dataframe(df_selected)

    fig2 = make_subplots(rows=len(selected_cols), cols=1, subplot_titles=selected_cols, vertical_spacing=0.1,
                         horizontal_spacing=0.00)
    fig2.update_layout(height=len(selected_cols) * 250, width=1000, showlegend=False,
                       margin=dict(l=0, r=0, t=30, b=0))

    for i, col in enumerate(selected_cols):

        if col=='glucose':
            fig2.add_trace((go.Scatter(x=df_selected['timestamp'], y=df_selected[col], name=col, mode='lines',
                                       hovertext=df_selected['menu'],
                                       hovertemplate="datetime : %{x}<br>" + "glucose : %{y}<br>" +
                                                     "meal : %{hovertext}<br>",
                                       line=dict(color=px.colors.qualitative.G10[i], width=1))), row=i + 1, col=1)
            fig2.add_hrect(y0=TIR_range[0], y1=TIR_range[1], fillcolor = 'red', opacity=0.1, line_width = 0, row=i+1, col=1)

        elif col in ['meal', 'activity', 'alcohol']:
            key_val = {'meal':'menu', 'activity':'act_type', 'alcohol':'alcohol_type'}
            fig2.add_trace((go.Scatter(x=df_selected['timestamp'], y=df_selected[col], name=col, mode='lines',
                                       hovertext=df_selected[key_val[col]],
                                       hovertemplate="datetime : %{x}<br>" +
                                                     "%{hovertext}<br>",
                                       line=dict(color=px.colors.qualitative.G10[i], width=1))), row=i + 1, col=1)

        elif col in ['meal_intensity', 'act_intensity', 'alcohol_intensity']:
            key_val = {'meal_intensity': 'menu', 'act_intensity': 'act_type', 'alcohol_intensity': 'alcohol_type'}
            fig2.add_trace((go.Scatter(x=df_selected['timestamp'], y=df_selected[col], name=col, mode='lines',
                                       hovertext=df_selected[key_val[col]],
                                       hovertemplate="datetime : %{x}<br>" +
                                                     "%{hovertext}<br>",
                                       line=dict(color=px.colors.qualitative.G10[i], width=1))), row=i + 1, col=1)

        else:
            fig2.add_trace((go.Scatter(x=df_selected['timestamp'], y=df_selected[col], name=col, mode='lines',
                                       hovertemplate="datetime : %{x}<br>" + "%{y}<br>",
                                       line=dict(color=px.colors.qualitative.G10[i], width=1))), row=i + 1, col=1)

    st.plotly_chart(fig2, use_container_width=True)


  ################################## FOOTER ##################################

st.markdown('-----------------------------------------------------')
st.text('Developed by GIVITA AI part - 2022')
st.text('Mail: help@gi-vita.io')