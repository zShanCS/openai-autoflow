import os

import openai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_code(prompt, **kwargs):
    '''
    Useful parameters
        - temperature/top_p
        - best_of
        - max_tokens
        - frequency_penalty
        - presence_penalty
        - stop
        - n
    '''
    default_kwargs = {
        "top_p": 1.0,
        "max_tokens": 256,
    }
    # set default value if not present in kwargs
    for k, v in default_kwargs.items():
        if k not in kwargs:
            kwargs[k] = v
    result = openai.Completion.create(
        engine="code-davinci-001",
        prompt=prompt,
        **kwargs
    )
    if 'n' in kwargs:
        codes = []
        for code in result["choices"]:
            code = code["text"].split("\n")
            code = list(filter(lambda x: x != '', code))
            code = "\n".join(code)
            codes.append(code)
        return codes
    else:
        code = result["choices"][0]["text"].split("\n")
        code = list(filter(lambda x: x != '', code))
        code = "\n".join(code)
        return code
