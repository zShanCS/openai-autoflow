import os

import openai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_code(prompt, get_fn_reason=False, **kwargs):
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
        # [(code, finish_reason)]
        for item in result["choices"]:
            finish_reason = item['finish_reason']
            code = item["text"]
            if get_fn_reason:
                codes.append((code, finish_reason))
            else:
                codes.append(code)
        return codes
    else:
        finish_reason = result['choices'][0]['finish_reason']
        code = result["choices"][0]["text"]
        if get_fn_reason:
            return code, finish_reason
        else:
            return code


def iteratively_request_code(prompt, **kwargs):
    '''Request Codex for code until finish_reason == stop'''
    code, fn_reason = get_code(prompt, get_fn_reason=True, **kwargs)
    # iteratively send requests
    if fn_reason == "length":
        num_reqs = 0
        # max_tokens for resend is capped at 64
        kwargs['max_tokens'] = 64
        # get the length of the template to strip it off later
        initial_length = len(prompt)
        # send no more than 3 additional reqs due to usage limits
        while fn_reason == "length" and num_reqs < 3:
            prompt += code
            code, fn_reason = get_code(prompt, get_fn_reason=True, **kwargs)
            num_reqs += 1
        # add the last part
        prompt += code
        # remove the template
        return prompt[initial_length:]
    # return original code
    return code
