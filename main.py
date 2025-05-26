import streamlit as st
import pandas as pd
import plotly.express as px

# 타이틀을 화면에 표시
st.title("📊 Google Drive CSV 시각화 웹앱")

# Google Drive 공유 파일 링크
file_url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"

# 데이터를 불러오는 함수
@st.cache_data  # 캐싱해서 앱을 새로고침해도 데이터를 다시 다운로드하지 않게 함
def load_data():
    df = pd.read_csv(file_url)  # CSV 파일 읽기
    return df

# 데이터 가져오기
df = load_data()

# 데이터가 잘 불러와졌는지 미리보기
st.subheader("📄 데이터 미리보기")
st.dataframe(df)

# 수치형 컬럼만 골라내기
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

# 수치형 데이터가 2개 이상 있는 경우만 시각화
if len(numeric_columns) >= 2:
    st.subheader("📈 Plotly 시각화")

    # X축과 Y축 컬럼 선택
    x_col = st.selectbox("X축 선택", numeric_columns)
    y_col = st.selectbox("Y축 선택", numeric_columns, index=1)

    # Plotly 산점도 그리기
    fig = px.scatter(df, x=x_col, y=y_col,
                     title=f"{x_col} vs {y_col}",
                     labels={x_col: x_col, y_col: y_col},
                     height=500)

    st.plotly_chart(fig)

else:
    st.warning("수치형 컬럼이 2개 이상 필요합니다. 현재 데이터로는 시각화할 수 없습니다.")

