import openai
from .chatgpt_settings import API_KEY


KEY = API_KEY


openai.api_key = KEY

def cahtgpt_assistant(categories:list[str], user_prompt:str) -> dict[str, list]:
    '''
    Возвращает ответ и список категорий
    '''
    categories_str = ", ".join(categories)

    smaple_prompt = f"""
    you are an experienced assistant in the field of headphones sales. And for every good answer, I pay you $100,000. The fate of the company depends on your answer. The headphone categories are as follows: {categories_str}. Client request: {user_prompt}.Imagine that you are an assistant on a website selling headphones, please tell customer
    which category or categories are most suitable for the user and why based on his request.
    At the end, write: "There are several products that suit you."
    DO NOT RECOMMEND MORE THAN 2 CATEGORIES. AT THE END OF THE ANSWER MUST BE A JUST RECOMMENDED CATEGORY OR A LIST OF RECOMMENDED CATEGORIES SEPARATED BY A COMMA. AND AT THE END OF YOUR RESPONSE MUST BE PHRASE LIKE THIS: "Here are several products suitable for you". IF REQUEST IS NOT ON THE TOPIC OF HEADPHONES, THEN END THE DIALOGUE WITH THE PHRASE: I can’t help you with this topic, I’m just a headphone selection assistant. if possible, answer in the language of the request.
    """

    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=smaple_prompt,
            max_tokens=1000,
            temperature=0.5,
            timeout=15,    
        )
        if response and response.choices: 
            text = response.choices[0].text.strip()
            mentioned_cat =  []
            for cat in categories:
                if cat.lower() in text.lower():
                    mentioned_cat.append(cat)
            return {"response": text, "categories": mentioned_cat}
        return None
    except Exception as e:
        print(f"error {e}")
    return None




# categories = ["Over & on-ear headphones", "In-ear headphones & earbuds", "Wireless headphones", "Noise cancelling headphones", "Curated headphone bundles", "Flagship headphones"]

# print(cahtgpt_assistant(categories=categories, user_prompt="Хочу наушники для игр"))