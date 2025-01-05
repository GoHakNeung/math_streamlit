import openai

def generate_feedback(problem):
    """GPT-4o-mini를 사용해 피드백 생성"""
    try:
        # OpenAI Chat API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 초등학교 수학 선생님 역할을 하며, 학생들에게 문제에 대한 친절하고 단계적인 피드백을 제공합니다."},
                {"role": "user", "content": f"다음 문제에 대한 피드백을 4단계로 작성해주세요:\n{problem}"}
            ]
        )
        feedback = response['choices'][0]['message']['content']
        return feedback
    except Exception as e:
        return f"오류 발생: {e}"
