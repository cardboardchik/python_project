import openai

KEY = 'sk-proj-XngTThEDCAarCcByuoMUT3BlbkFJS84tkobwD8gP7RbVVwye'


openai.api_key = KEY

def request_response(user_prompt):
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_prompt,
            max_tokens=1000,
            temperature=0.5,
            stop=["\n\n"],
            timeout=15,    
        )
        if response and response.choices: 
            return response.choices[0].text.strip()
        return None
    except Exception as e:
        print(f"error {e}")
    return None