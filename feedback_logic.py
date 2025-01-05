import openai

def generate_feedback(problem):
    """GPT-4o-mini를 사용해 피드백 생성"""
    try:
        # OpenAI Chat API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            system_prompt = """
            너는 초등학생에 문제해결을 위한 피드백을 주는 역할을 한다. 
            만약 수학과 관련없는 내용이 나오면 '초등학교 수학 문제를 물어보세요.'를 출력합니다. 
            피드백은 4단계로 제공된다. 1단계는 학생들이 문제를 이해할 수 있도록 도와준다. 2단계는 문제와 관련된 개념을 설명해 준다. 3단계는 문제 해결에 필요한 식 또는 풀이 방법을 제공해준다. 4단계는 3단계에서 제공한 식 또는 풀이 방법에 문제에서 제시된 값을 넣어서 학생들이 풀 수 있도록 한다. 
            구체적인 답을 주면 안되고 풀수 있도록 도와줘야 한다. 
            형식은 1~4단계를 붙여서 피드백을 줘. 
            """,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"다음 문제에 대한 피드백을 4단계로 작성해주세요:\n{problem}"}
            ]
        )
        feedback = response['choices'][0]['message']['content']
        return feedback
    except Exception as e:
        return f"오류 발생: {e}"
