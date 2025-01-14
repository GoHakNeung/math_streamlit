import streamlit as st
import openai
from feedback_logic import generate_feedback
import requests
from PIL import Image
from streamlit_cropper import st_cropper

# OpenAI API 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]
ocrspaceapi = st.secrets["ocr_space_api"]

# Streamlit 기본 구성
st.set_page_config(page_title="Math Feedback Service", layout="wide")
st.title("초등학교 수학 문제 피드백 서비스")

# 상태 초기화
if "additional_info_visible" not in st.session_state:
    st.session_state["additional_info_visible"] = False
if "additional_info_content" not in st.session_state:
    st.session_state["additional_info_content"] = ""
if "camera_mode" not in st.session_state:
    st.session_state["camera_mode"] = False  # 카메라 비활성화 상태
if "image" not in st.session_state:
    st.session_state["image"] = None  # 촬영된 이미지
if "cropped_image" not in st.session_state:
    st.session_state["cropped_image"] = None  # 자른 이미지

# 버튼 레이아웃 설정
col1, col2 = st.columns(2)

# 촬영 버튼
with col1:
    if st.button("촬영"):
        st.session_state["camera_mode"] = True  # 카메라 모드 활성화
        st.session_state["cropped_image"] = None  # 이전 자른 이미지 초기화

# 피드백 생성 버튼
with col2:
    if st.button("피드백 생성"):
        problem = st.text_area("수학 문제를 입력하세요:", placeholder="예: 직각삼각형 모양의 종이를 돌려 원뿔을 만들었을 때...")
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

# OCR API 호출 함수
def ocr_space_api(image, api_key=ocrspaceapi):
    url = "https://api.ocr.space/parse/image"
    files = {"file": image}
    data = {"apikey": api_key, "language": "kor"}
    response = requests.post(url, files=files, data=data)
    result = response.json()
    return result.get("ParsedResults")[0]["ParsedText"] if "ParsedResults" in result else "OCR 실패"

# 이미지 처리 및 피드백 생성 칼럼
col = st.container()

with col:
    # 카메라 입력 (사진 촬영)
    if st.session_state["camera_mode"]:
        st.subheader("📷 사진을 촬영하세요")
        image = st.camera_input("카메라로 문제를 캡처하세요")
        if image:
            st.session_state["image"] = Image.open(image)
            st.session_state["camera_mode"] = False  # 카메라 모드 비활성화
            st.success("사진이 성공적으로 캡처되었습니다!")

    # 이미지 자르기 및 완료 처리
    if st.session_state["image"] and not st.session_state["camera_mode"]:
        st.subheader("이미지를 자르세요")
        cropped_img = st_cropper(
            st.session_state["image"],
            realtime_update=True,
            box_color="blue",
            aspect_ratio=None
        )

        # 자른 이미지 표시
        st.image(cropped_img, caption="자른 이미지", use_container_width=True)

        # 완료 버튼
        if st.button("완료"):
            st.session_state["cropped_image"] = cropped_img  # 자른 이미지를 저장
            st.session_state["image"] = None  # 원본 이미지를 초기화
            st.session_state["camera_mode"] = False  # 카메라 모드 비활성화
            st.success("이미지 처리가 완료되었습니다!")

    # 자른 이미지 최종 표시
    if st.session_state["cropped_image"]:
        st.image(st.session_state["cropped_image"], caption="최종 자른 이미지", use_container_width=True)
