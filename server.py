from fastapi import FastAPI
from server_models import API_Req, Code_Task, Prompt, Prompt_Language, IntentAnalysis, QueryInfo
from code_gen import iteratively_request_code
from templates import (code2nl, fix_bugs, get_api_request_code,
                       get_error_explanation, nl2sql, sql2nl, code2docstring, get_oneliner, code2ut, complete_code)

'''
    code2nl, ☑️
    fix_bugs, ☑️
    get_api_request_code, ☑️
    get_error_explanation, ☑️
    nl2sql, ☑️
    sql2nl, ☑️
    code2docstring, ☑️
    get_oneliner, ☑️
    code2ut, ☑️
    complete_code ☑️
'''
app = FastAPI()


@app.post('/code2nl')
async def codeToNl(data: Prompt_Language):
    print(data)
    return {'status': 'ok', 'output': code2nl(data.prompt, data.language)}


@app.post('/fix_bugs')
async def FixBugs(data: Prompt_Language):
    print(data)
    return {'status': 'ok', 'output': fix_bugs(data.prompt, data.language)}


@app.post('/explain_error')
async def GetErrorExplanation(data: Prompt):
    print(data)
    return {'status': 'ok', 'output': get_error_explanation(data.prompt)}


@app.post('/sql2nl')
async def SQL_to_NL(data: Prompt):
    print(data)
    return {'status': 'ok', 'output': sql2nl(data.prompt)}


@app.post('/oneliner')
async def One_Liner(data: Prompt_Language):
    print(data)
    return {'status': 'ok', 'output': get_oneliner(data.prompt, data.language)}


@app.post('/code2docstring')
async def Code2DocString(data: Prompt):
    print(data)
    return {'status': 'ok', 'output': code2docstring(data.prompt)}


@app.post('/code2ut')
async def Code2DUnitTest(data: Prompt_Language):
    print(data)
    return {'status': 'ok', 'output': code2ut(data.prompt, data.language)}


@app.post('/complete_code')
async def CodeCompletion(data: Code_Task):
    print(data)
    return {'status': 'ok', 'output': complete_code(data.code, data.task)}


@app.post('/nl2sql')
async def NLtoSQL(data: QueryInfo):
    columnList = []
    print(data)
    tableNames = data.tableName.split(",")
    columnNames = data.columnName.split("]")
    for cols in columnNames:
        columnList.append(cols.split(","))
    return {'status': 'ok', 'output': nl2sql(tableNames, columnNames, data.task)}


@app.post('/api_req')
async def Api_Request(data: API_Req):
    print(data)
    return {'status': 'ok', 'output': get_api_request_code(data.api_name, data.task, data.params, data.token)}


@app.post('/magic')
async def Api_Request(data: Prompt):
    print(data)
    return {'status': 'ok', 'output': iteratively_request_code(prompt=data.prompt, temperature=0.8, frequency_penalty=1, presence_penalty=0.5,
                                                               max_tokens=512, stop=['\n\n\n'], best_of=5)}


@app.post('/intent')
async def get_intent(query: IntentAnalysis):
    queryStr = query.query
    print(queryStr)
    intent_list = set()
    if queryStr.lower().find('code') != -1:
        intent_list.add('code2nl')

    if queryStr.lower().find('sql') != -1:
        intent_list.add('sql2nl')
        intent_list.add('nl2sql')

    if queryStr.lower().find('bugs') != -1:
        intent_list.add('fix_bugs')
        intent_list.add('get_error_explanation')

    if queryStr.lower().find('error') != -1:
        intent_list.add('get_error_explanation')

    if queryStr.lower().find('one') != -1:
        intent_list.add('get_oneliner')
    if queryStr.lower().find('shorten') != -1:
        intent_list.add('get_oneliner')

    if queryStr.lower().find('docstring') != -1:
        intent_list.add('code2docstring')
    if queryStr.lower().find('documentation') != -1:
        intent_list.add('code2docstring')

    if queryStr.lower().find('test') != -1:
        intent_list.add('code2ut')

    if queryStr.lower().find('complete') != -1:
        intent_list.add('complete_code')

    if queryStr.lower().find('api') != -1:
        intent_list.add('get_api_request_code')
    if queryStr.lower().find('request') != -1:
        intent_list.add('get_api_request_code')

    if len(intent_list) == 0:
        return {'status': 'ok', 'output': ['magic']}
    return {'status': 'ok', 'output': list(intent_list)}