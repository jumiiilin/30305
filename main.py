import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 제목
st.title("Google Drive CSV 시각화 (Plotly)")

# 데이터 URL (Google Drive 공유 링크)
file_url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(file_url)
    return df

df = load_data()

st.subheader("데이터 미리보기")
st.write(df.head())

# 시각화 (예시: 수치형 컬럼 간 산점도)
numeric_cols = df.select_dtypes(include='number').columns.tolist()

if len(numeric_cols) >= 2:
    x_axis = st.selectbox("X축", numeric_cols)
    y_axis = st.selectbox("Y축", numeric_cols, index=1)
    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
    st.plotly_chart(fig)
else:
    st.warning("수치형 컬럼이 부족하여 시각화를 할 수 없습니다.")
