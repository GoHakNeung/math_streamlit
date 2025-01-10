import streamlit as st
import openai
from feedback_logic import generate_feedback
import pytesseract
from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor

image = Image.open(IMAGE_PATH)
langs = ["en"] # Replace with your languages - optional but recommended
det_processor, det_model = load_det_processor(), load_det_model()
rec_model, rec_processor = load_rec_model(), load_rec_processor()

predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)

# OpenAI API 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]




# Streamlit 기본 구성
st.set_page_config(page_title="Math Feedback Service", layout="wide")
st.title("초등학교 수학 문제 피드백 서비스")

# 상태 초기화
if "additional_info_visible" not in st.session_state:
    st.session_state["additional_info_visible"] = False
if "additional_info_content" not in st.session_state:
    st.session_state["additional_info_content"] = ""
if "camera_mode" not in st.session_state:
    st.session_state["camera_mode"] = False  # 카메라 모드 활성화 상태

# 문제 입력 영역
problem = st.text_area("수학 문제를 입력하세요:", placeholder="예: 직각삼각형 모양의 종이를 돌려 원뿔을 만들었을 때...")

# 피드백 요청 버튼
if st.button("피드백 생성"):
    if problem.strip():
        with st.spinner("피드백을 생성 중입니다..."):
            feedback, requires_more_info = generate_feedback(problem)

            if requires_more_info:
                st.warning("문제를 해결하기 위한 추가 정보가 필요합니다. 아래에 추가 정보를 입력하세요.")
                st.session_state["additional_info_visible"] = True
            else:
                st.subheader("생성된 피드백:")
                st.markdown(feedback)
    else:
        st.warning("문제를 입력해주세요!")

# 추가 정보 입력 영역 (상태 기반으로 표시)
if st.session_state["additional_info_visible"]:
    additional_info = st.text_area(
        "문제에 대한 추가 정보를 입력하세요:",
        value=st.session_state["additional_info_content"],  # 유지된 값을 사용
        key="additional_info_input"
    )

    # 상태 업데이트 버튼 클릭 시 저장
    if st.button("추가 정보를 포함한 피드백 생성"):
        st.session_state["additional_info_content"] = additional_info  # 입력된 값을 상태에 저장
        combined_input = f"문제: {problem}\n추가 정보: {st.session_state['additional_info_content']}"
        with st.spinner("피드백을 생성 중입니다..."):
            feedback, _ = generate_feedback(combined_input)
            st.subheader("생성된 피드백:")
            st.markdown(feedback)

# 카메라 입력 영역
camera_button_label = "📷"
langs = ["ko"] # Replace with your languages - optional but recommended
det_processor, det_model = load_det_processor(), load_det_model()
rec_model, rec_processor = load_rec_model(), load_rec_processor()

if st.button(camera_button_label):
    if not st.session_state["camera_mode"]:
        st.session_state["camera_mode"] = True  # 카메라 모드 활성화
    else:
        st.session_state["camera_mode"] = False  # 촬영 완료 후 비활성화

if st.session_state["camera_mode"]:
    image = st.camera_input("카메라로 문제를 캡처하세요")
    if image:
        predictions = run_ocr([image], [langs], det_model, det_processor, rec_model, rec_processor)

        st.text_area("추출된 텍스트:", value=predictions, height=200)
    else:
        st.warning("이미지를 캡처해주세요!")



