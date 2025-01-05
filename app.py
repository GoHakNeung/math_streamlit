import streamlit as st
import openai
from feedback_logic import generate_feedback

# OpenAI API 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Streamlit Secrets 사용

# Streamlit 기본 구성
st.set_page_config(page_title="Math Feedback Service", layout="wide")
st.title("초등학교 수학 문제 피드백 서비스")
st.title(st.secrets["OPENAI_API_KEY"])
# 문제 입력란
problem = st.text_area("수학 문제를 입력하세요:", placeholder="예: 직각삼각형 모양의 종이를 돌려 원뿔을 만들었을 때...")

# 피드백 요청 버튼
if st.button("피드백 생성"):
    if problem.strip():
        with st.spinner("피드백을 생성 중입니다..."):
            feedback = generate_feedback(problem)
            st.subheader("생성된 피드백:")
            st.write(feedback)
    else:
        st.warning("문제를 입력해주세요!")
