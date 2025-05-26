import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------
# 🔹 설정: 페이지 기본 레이아웃
# --------------------------------------
st.set_page_config(page_title="CSV Plotly 시각화", layout="wide")

st.title("📊 Google Drive CSV Plotly 시각화 앱")
st.markdown("데이터를 Google Drive에서 불러와 Plotly로 시각화합니다.")

# --------------------------------------
# 🔹 데이터 불러오기 함수
# --------------------------------------
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {e}")
        return None

# --------------------------------------
# 🔹 Google Drive 공유 링크 입력
# --------------------------------------
default_url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"
file_url = st.text_input("📂 Google Drive 공유 링크 (직접 수정 가능)", value=default_url)

# 데이터 로드
df = load_data(file_url)

if df is not None:
    st.subheader("🧾 데이터 미리보기")
    st.dataframe(df, use_container_width=True)

    # --------------------------------------
    # 🔹 수치형 및 범주형 컬럼 분리
    # --------------------------------------
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    category_cols = df.select_dtypes(include="object").columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("⚠️ 시각화를 위해 수치형 컬럼이 최소 2개 이상 필요합니다.")
    else:
        # --------------------------------------
        # 🔹 사용자 옵션 선택
        # --------------------------------------
        st.sidebar.header("🛠️ 시각화 설정")

        graph_type = st.sidebar.selectbox("그래프 유형 선택", ["산점도", "히스토그램", "박스 플롯"])

        x_axis = st.sidebar.selectbox("X축", numeric_cols)
        y_axis = st.sidebar.selectbox("Y축", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)

        color = st.sidebar.selectbox("색상 구분 (옵션)", [None] + category_cols + numeric_cols)
        size = st.sidebar.selectbox("크기 기준 (옵션)", [None] + numeric_cols)

        # --------------------------------------
        # 🔹 Plotly 그래프 생성
        # --------------------------------------
        fig = None

        if graph_type == "산점도":
            fig = px.scatter(
                df, x=x_axis, y=y_axis,
                color=color if color != "None" else None,
                size=size if size != "None" else None,
                title=f"{x_axis} vs {y_axis} (산점도)",
                height=600
            )
        elif graph_type == "히스토그램":
            fig = px.histogram(
                df, x=x_axis,
                color=color if color != "None" else None,
                title=f"{x_axis} 분포 (히스토그램)",
                height=600
            )
        elif graph_type == "박스 플롯":
            fig = px.box(
                df, x=color if color != "None" else None, y=y_axis,
                title=f"{y_axis} (박스 플롯)",
                height=600
            )

        if fig:
            st.subheader("📈 결과 그래프")
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 상단에 유효한 Google Drive CSV 링크를 입력해주세요.")
