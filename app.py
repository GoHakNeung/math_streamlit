# ocr_space_api 버전, 성능은 ? 
# 사진을 가로로 찍었을 때, 회전 기능 필요함.
import streamlit as st
import openai
from feedback_logic import generate_feedback
import requests
from PIL import Image

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
    st.session_state["camera_mode"] = False  # 카메라 모드 활성화 상태
if "rotation_angle" not in st.session_state:
    st.session_state["rotation_angle"] = 0  # 회전 각도 저장

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
def ocr_space_api(image, api_key=ocrspaceapi):
    url = "https://api.ocr.space/parse/image"
    files = {"file": image}
    data = {"apikey": api_key, "language": "kor"}
    response = requests.post(url, files=files, data=data)
    result = response.json()
    return result.get("ParsedResults")[0]["ParsedText"] if "ParsedResults" in result else "OCR 실패"


if st.button(camera_button_label):
    if not st.session_state["camera_mode"]:
        st.session_state["camera_mode"] = True  # 카메라 모드 활성화
    else:
        st.session_state["camera_mode"] = False  # 촬영 완료 후 비활성화

if st.session_state.get("camera_mode", False):
    image = st.camera_input("카메라로 문제를 캡처하세요")
    if image:
        st.session_state["image"] = Image.open(image)  # PIL 이미지로 저장
        st.session_state["rotation_angle"] = 0  # 초기 회전 각도로 설정
        st.success("이미지가 성공적으로 캡처되었습니다!")

    if st.session_state["image"]:
        # 회전 버튼
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 90도 회전"):
                st.session_state["rotation_angle"] += 90
                st.session_state["rotation_angle"] %= 360  # 360도 이상이면 0으로 순환
        with col2:
            if st.button("완료"):
                # OCR 실행
                with st.spinner("텍스트 추출 중..."):
                    buffer = BytesIO()
                    rotated_image = ImageOps.exif_transpose(st.session_state["image"].rotate(st.session_state["rotation_angle"]))
                    rotated_image.save(buffer, format="PNG")
                    buffer.seek(0)
                    text = ocr_space_api(buffer)
                st.text_area("추출된 텍스트:", value=text, height=200)
    
        # 회전된 이미지 표시
        rotated_image = ImageOps.exif_transpose(st.session_state["image"].rotate(st.session_state["rotation_angle"]))
        st.image(rotated_image, caption=f"회전 각도: {st.session_state['rotation_angle']}°", use_column_width=True)
    
    else:
        st.button("📷 카메라 열기", on_click=lambda: st.session_state.update({"camera_mode": True}))
        

    # if image:
    #     st.success("이미지가 성공적으로 캡처되었습니다!")
    #     # st.image(image)  # 캡처된 이미지를 출력
    #     # # 추가 처리 로직을 여기 추가할 수 있습니다.
    #     with st.spinner("텍스트 추출 중..."):
    #         text = ocr_space_api(image)
    #         st.text_area("추출된 텍스트:", value=text, height=200)
    #         # img = Image.open(image)


    # else:
    #     st.warning("이미지를 캡처해주세요!")
