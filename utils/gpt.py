import json
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
import time
import os
from typing import Union, List, Optional
from utils.config import OPENAI_API_KEY
from utils.t import SubmissionInfo

class OpenAIGPT():

    def __init__(
            self, 
            model_name : str, 
            api_key : str) -> None:
        """
        Args:
            model_name (str) ~ api_key (str): 参见BaseModel的__init__方法
        """
        self.model_name = model_name
        self.api_key = api_key

    @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
    def complete_messages(
        self, 
        messages : List[dict], 
        functions : Optional[List[dict]] = None, 
        try_time : int = 6, 
        try_sleep_time : int = 15,
        **args
        ) -> dict:
        """
        Args:
            messages (List[dict]) ~ functions (List[dict]): 参见BaseModel的complete_messages方法  
            try_time (int): try time of one request
            try_sleep_time (int): sleep time between two requests
            args (dict): other args
        Returns:
            new_response (dict): 参见BaseModel的complete_messages方法
        """
        for _ in range(try_time):
            if _:
                time.sleep(try_sleep_time)
            openai.api_key = self.api_key
            if not functions:
                new_response = openai.ChatCompletion.create(
                    model = self.model_name,
                    messages = messages,
                    **args
                    )
            else:
                new_response = openai.ChatCompletion.create(
                    model = self.model_name,
                    messages = messages, 
                    functions=functions, 
                    **args
                    )
            
            total_tokens = new_response['usage']['total_tokens'] # type: ignore
            prompt_tokens = new_response['usage']['prompt_tokens'] # type: ignore
            completion_tokens = new_response['usage']['completion_tokens'] # type: ignore
            new_message = new_response['choices'][0]["message"] # type: ignore
            ret = {
                "total_tokens": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "message": new_message
            }
            return ret
        raise Exception("OpenAI API Error")
            # try:
            #     total_tokens = new_response['usage']['total_tokens']
            #     prompt_tokens = new_response['usage']['prompt_tokens']
            #     completion_tokens = new_response['usage']['completion_tokens']
            #     new_message = new_response['choices'][0]["message"]
            #     ret = {
            #         "total_tokens": total_tokens,
            #         "prompt_tokens": prompt_tokens,
            #         "completion_tokens": completion_tokens,
            #         "message": new_message
            #     }
            #     return ret
            # except openai.error.APIError as e:
            #     print(f"OpenAI API returned an API Error: {e}")
            # except openai.error.Timeout as e:
            #     print(f"OpenAI API returned a Timeout Error: {e}")
            # except openai.error.RateLimitError as e:
            #     print(f"OpenAI API returned a RateLimit Error: {e}")
            #     time.sleep(self.try_sleep_time)
            # except openai.error.APIConnectionError as e:
            #     print(f"OpenAI API returned an APIConnection Error: {e}")
            # except openai.error.InvalidRequestError as e:
            #     print(f"OpenAI API returned an InvalidRequest Error: {e}")
            # except openai.error.AuthenticationError as e:
            #     print(f"OpenAI API returned an Authentication Error: {e}")
            #     raise e
            # except openai.error.ServiceUnavailableError as e:
            #     print(f"OpenAI API returned a ServiceUnavailable Error: {e}")
            # except Exception as e:
            #     print(f"OpenAI calling Exception: {e}")
            #     raise e

def gpt_service(submission_info: SubmissionInfo):
    model_name = "gpt-3.5-turbo"
    api_key = OPENAI_API_KEY
    llm = OpenAIGPT(model_name, api_key)
    description = submission_info.problem_info.problem_description + "\n" + submission_info.problem_info.input_description + "\n" + submission_info.problem_info.output_description

    sample_description = submission_info.problem_info.sample_input_description + "\n" + submission_info.problem_info.sample_output_description

    source_code = submission_info.source_code
    code_state = submission_info.status

    messages = [
        {"role": "system", "content": "我希望你假定自己是一个擅长在线编程解题的人，你将解释OpenJudge提交的错误原因。用户会给你一个OpenJudge的提交记录，包括题目描述、样例的描述、用户的代码和用户代码的提交状态（提交状态可能是Accepted、Runtime Error等等，Accepted代表用户的代码正确，Runtime Error代表用户的代码运行时出现了错误），你需要解释这个提交为什么会出错。你需要解释的内容包括：\n1. 代码的错误原因\n2. 代码的改进方案\n3. 代码的改进后的样子，并为每一行添加注释\n\n请在回答中写出以上三点，不要写解释。"},
        {"role": "user", "content": f"""
题目的描述是: {description}
样例的描述是: {sample_description}
用户的代码是: {source_code}
用户代码的提交状态是: {code_state}
"""},
    ]
    # role: assistant
    output = llm.complete_messages(messages)
    return json.dumps(output, indent=4, ensure_ascii=False)
    # print(json.dumps(output, indent=4, ensure_ascii=False))
    # 输出类似
    # {
    #     "total_tokens": 89,
    #     "prompt_tokens": 19,
    #     "completion_tokens": 70,
    #     "message": {
    #         "role": "assistant",
    #         "content": "I'm sorry, but as an AI language model, I don't have access to real-time or specific team data. Therefore, I cannot provide you with information about the previous tournaments of a specific team named \"Rocket.\" I suggest searching online or referring to dedicated eSports or gaming websites for accurate and up-to-date information on team Rocket's tournament history."
    #     }
    # }