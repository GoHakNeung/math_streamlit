import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import pytesseract
import openai
from feedback_logic import generate_feedback


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
if "camera_active" not in st.session_state:
    st.session_state["camera_active"] = False

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

# OCR 기능 추가
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    def transform(self, frame):
        self.frame = frame.to_ndarray(format="bgr24")
        return self.frame

def extract_text_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

st.header("OCR 기능")

if st.session_state["camera_active"]:
    webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)
    if webrtc_ctx.video_transformer:
        if st.button("📸 촬영"):
            image = webrtc_ctx.video_transformer.frame
            if image is not None:
                st.image(image, caption="Captured Image", use_column_width=True)
                text = extract_text_from_image(image)
                st.subheader("Extracted Text")
                st.session_state["additional_info_content"] = text
                st.write(text)
                st.session_state["camera_active"] = False
            else:
                st.warning("No frame captured")
else:
    if st.button("📷 Start Camera"):
        st.session_state["camera_active"] = True
