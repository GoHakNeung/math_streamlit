import streamlit as st
import openai
from feedback_logic import generate_feedback

# OpenAI API 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit 기본 구성
st.set_page_config(page_title="Math Feedback Service", layout="wide")
st.title("초등학교 수학 문제 피드백 서비스")

# 기본 입력 영역
problem = st.text_area("수학 문제를 입력하세요:", placeholder="예: 직각삼각형 모양의 종이를 돌려 원뿔을 만들었을 때...")

# 피드백 요청 버튼
if st.button("피드백 생성"):
    if problem.strip():
        with st.spinner("피드백을 생성 중입니다..."):
            # 문제에 대해 피드백 생성
            feedback, requires_more_info = generate_feedback(problem)
            
            if requires_more_info:
                st.warning("문제를 해결하기 위한 추가 정보가 필요합니다. 아래에 추가 정보를 입력하세요.")
                
                # 새로운 입력 영역 추가
                additional_info = st.text_area("문제에 대한 추가 정보를 입력하세요:", key="additional_info")

                if st.button("추가 정보를 포함한 피드백 생성"):
                    # 기존 문제와 추가 정보를 결합하여 피드백 생성
                    combined_input = f"문제: {problem}\n추가 정보: {additional_info.strip()}"
                    st.write(combined_input)
                    with st.spinner("피드백을 생성 중입니다..."):
                        feedback, _ = generate_feedback(combined_input)
                        st.subheader("생성된 피드백:")
                        st.write(feedback)
            else:
                # 충분한 정보로 피드백 생성
                st.subheader("생성된 피드백:")
                st.write(feedback)
    else:
        st.warning("문제를 입력해주세요!")
