from fastapi import FastAPI
from server_models import API_Req, Code_Task, Prompt, Prompt_Language, IntentAnalysis, QueryInfo
from code_gen import iteratively_request_code
from classify_intent import get_task_from_query
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
    intent_list = get_task_from_query(queryStr)
    if len(intent_list) == 0:
        return {'status': 'ok', 'output': ['magic']}
    return {'status': 'ok', 'output': list(intent_list)}
