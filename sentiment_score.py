import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
import os

GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4"
GPT4_turbo = 'gpt-4-1106-preview'

class GPT4QAModel():
    def __init__(self, model=GPT4):
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        self.model = model

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _attempt_answer_question(self, question, max_tokens=2000, stop_sequence=None):
        response = openai.ChatCompletion.create(
          model=self.model,
          messages=[
                {"role": "system", "content": "You are Question Answering Portal"},
                {"role": "user", "content": question}
            ],
          temperature=0
        )
        return response["choices"][0]['message']['content'].strip()

    @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(6))
    def answer_question(self, question, max_tokens=2000, stop_sequence=None):
        try:
            return self. _attempt_answer_question(question, max_tokens=max_tokens, stop_sequence=stop_sequence)
        except Exception as e:
            print(e)


def bucket_score(score):
    return score

old_prompt = """
            You are a stock trading consultant. 
            You basically trade based on your gut feeling about market sentiment. 
            Your job is, given a news headline about a stock, assign a score to the strength of the stock. 
            The score can be a continuous value between 0 and 100. 
            0 means the stock is very weak and is going to show a bearish movement, and 
            100 means it is strong and will get a bullish movement. 
            Only output a single number. Here is the news: 
            """


def main():
    consultant = GPT4QAModel()
    new_prompt = '''
            You are a company specialist. 
            I want to know about the public opinion of a company. 
            Your job is to assign a score to a company from 0 to 100 based on its current opinion in the market. 
            Include things like its general opinion, profitability, recent news, controversies etc that may affect its value. 
            Output only a single number, nothing else. 
            0 means the company is in bad shape, 100 means company is in good shape.
            I don't need current score, it could be to whatever extent you are trained. 
            Here is the company:
            '''
    company = input("Enter Company: ")
    prompt = old_prompt + company
    response = consultant.answer_question(prompt)
    print(response)
    # if response.isdigit():
    #     score = int(response)
    # else:
    #     print('response corrupt. Assigning score of 50')
    #     score = 50
    # print(bucket_score(score))


if __name__ == '__main__':
    main()

    
