from copyreg import constructor
from fastapi import FastAPI
from server_models import Prompt_Language, IntentAnalysis
from templates import (code2nl, fix_bugs, get_api_request_code,
                       get_error_explanation, nl2sql, sql2nl, code2docstring, get_oneliner, code2ut,complete_code)

'''
    code2nl, ☑️
    fix_bugs,
    get_api_request_code,
    get_error_explanation
    nl2sql,
    sql2nl,
    code2docstring,
    get_oneliner,
    code2ut,
    complete_code
'''
app = FastAPI()

@app.post('/code2nl')
async def codeToNl(data:Prompt_Language):
    print(data)
    return {'status':'ok', 'output':code2nl(data.prompt, data.language)}

@app.post('/fix_bugs')
async def FixBugs(data:Prompt_Language):
    print(data)
    return {'status':'ok', 'output':fix_bugs(data.prompt, data.language)}

@app.post('/intent')
async def get_intent(query:IntentAnalysis):
    query = query.query
    intent_list = []
    if query.lower().find('code') != -1:
        intent_list.append('code2nl')
    if query.lower().find('sql') != -1:
        intent_list.extend(['sql2nl','nl2sql'])
    if query.lower().find('bugs') != -1:
        intent_list.extend(['fix_bugs'])
    
    if len(intent_list) == 0:
        return ['magic']
    return {'status':'ok', 'output':intent_list}