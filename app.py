import streamlit as st
import openai
from feedback_logic import generate_feedback

# OpenAI API 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Streamlit Secrets 사용

# Streamlit 기본 구성
st.set_page_config(page_title="Math Feedback Service", layout="wide")
st.title("초등학교 수학 문제 피드백 서비스")

# 첫 번째 질문 입력 영역
problem = st.text_area("수학 문제를 입력하세요:", placeholder="예: 직각삼각형 모양의 종이를 돌려 원뿔을 만들었을 때...")

# 추가 정보 입력 영역
additional_info = st.text_area("문제에 대한 추가 정보를 입력하세요:", placeholder="예: 학생의 학년, 문제에 대한 힌트 등 추가적인 정보를 입력하세요...")

# 피드백 요청 버튼
if st.button("피드백 생성"):
    if problem.strip():
        with st.spinner("피드백을 생성 중입니다..."):
            # 기존 문제와 추가 정보를 합침
            combined_input = f"문제: {problem}\n추가 정보: {additional_info.strip()}"
            feedback = generate_feedback(combined_input)
            st.subheader("생성된 피드백:")
            st.write(feedback)
    else:
        st.warning("문제를 입력해주세요!")
