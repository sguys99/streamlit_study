# 참고자료
# https://lucaseo.github.io/2020/03/13/20200313-1/


import streamlit as st
from PIL import Image

st.title('Streamlit Tutorial')

st.header('This is header')
st.subheader('This is subheader')

st.text('Hello Streamlit!!!')

## Markdown syntax
st.markdown("# This is a Markdown title")
st.markdown("## This is a Markdown header")
st.markdown("### This is a Markdown subheader")
st.markdown("- item 1\n"
            "   - item 1.1\n"
            "   - item 1.2\n"
            "- item 2\n"
            "- item 3")
st.markdown("1. item 1\n"
            "   1. item 1.1\n"
            "   2. item 1.2\n"
            "2. item 2\n"
            "3. item 3")

image = Image.open('files/eagle.jpg')
st.image(image, width = 400, caption = 'Image example: eagle')

vid_file = open('testvideo.mp4', 'rb')
video_bytes = vid_file.read()
st.video(vid_file, format = 'video/mp4', start_time=2)

st.success('Successful')
st.info('inforamtion')
st.warning('This is a warning')
st.error('This is an error!')
st.exception("NameError('Error name is not defined')")

st.markdown('### 데이터프레임과 테이블 출력')

import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)

iris_df['target'] = iris['target']
iris_df['target'] = iris_df['target'].apply(lambda x: \
                        'setosa' if x == 0 else ('versicolor' if x == 1 else 'virginica'))

st.table(iris_df.head())
st.dataframe(iris_df)
st.write(iris_df)

if st.checkbox('show/hide'):
    st.write('체크박스가 선택되었습니다.')

status = st.radio('Select status', ('Active', 'Inactive'))
if status == 'Active':
    st.success('활성화 되었습니다.')
else:
    st.warning('비활성화 되었습니다.')


## Select Box
occupation = st.selectbox("직군을 선택하세요.",
                          ["Backend Developer",
                           "Frontend Developer",
                           "ML Engineer",
                           "Data Engineer",
                           "Database Administrator",
                           "Data Scientist",
                           "Data Analyst",
                           "Security Engineer"])
st.write("당신의 직군은 ", occupation, " 입니다.")

## MultiSelect
location = st.multiselect("선호하는 유투브 채널을 선택하세요.",
                          ("운동", "IT기기", "브이로그",
                           "먹방", "반려동물", "맛집 리뷰"))
st.write(len(location), "가지를 선택했습니다.")


## Slider
level = st.slider("레벨을 선택하세요.", 1, 5)

## Buttons
if st.button("About"):
    st.text("Streamlit을 이용한 튜토리얼입니다.")


# Text Input
first_name = st.text_input("Enter Your First Name", "Type Here ...")
if st.button("Submit", key='first_name'):
    result = first_name.title()
    st.success(result)


# Text Area
message = st.text_area("메세지를 입력하세요.", "Type Here ...")
if st.button("Submit", key='message'):
    result = message.title()
    st.success(result)

## Date Input
import datetime
today = st.date_input("날짜를 선택하세요.", datetime.datetime.now())
the_time = st.time_input("시간을 입력하세요.", datetime.time())

## Sidebars
st.sidebar.header("사이드바 메뉴")
st.sidebar.selectbox("메뉴를 선택하세요.", ["데이터", "EDA", "코드"])

st.subheader('Matplotlib로 차트 그리기')
iris_df[iris_df['target']=='virginica']['petal length (cm)'].hist(bins = 20, color = 'r',
                                                                  alpha = 0.7)
st.pyplot()