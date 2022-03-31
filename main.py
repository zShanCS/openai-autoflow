import uvicorn
from fastapi import FastAPI

from classify_intent import get_task_from_query
from code_gen import iteratively_request_code
from nl2codes import search_for_code
from refactor_and_defect import detect_defect, refine
from server_models import (API_Req, Code_Task, IntentAnalysis, Prompt,
                           Prompt_Language, QueryInfo, SearchCode)
from templates import (code2docstring, code2nl, code2ut, complete_code,
                       fix_bugs, get_api_request_code, get_error_explanation,
                       get_oneliner, nl2sql, sql2nl)
from commit_bert import functions
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


@app.post('/refine')
async def Refine(data: Prompt):
    print(data)
    return {'status': 'ok', 'output': refine(data.prompt)}

@app.post('/commit-message')
async def commit_message(data: Prompt):
    print(data)
    return {'status': 'ok', 'output': functions.predict_message(data.prompt)}


@app.post('/detect-defect')
async def Api_Request(data: Prompt):
    print(data)
    return {'status': 'ok', 'output': detect_defect(data.prompt)}


@app.post('/search-code')
async def search_code(data: SearchCode):
    print(data.code)
    return {'status': 'ok', 'output': search_for_code(data.prompt, input_json=data.code, recreate=data.recreate)}



@app.post('/magic')
async def Api_Request(data: Prompt):
    print(data)
    return {'status': 'ok',
            'output': iteratively_request_code(prompt=f'"""{data.prompt}"""',
                                               temperature=0.6,
                                               frequency_penalty=0.5,
                                               presence_penalty=0.5,
                                               max_tokens=256,
                                               stop=['\n\n\n'],
                                               best_of=3)}


@app.post('/intent')
async def get_intent(query: IntentAnalysis):
    queryStr = query.query
    print(queryStr)
    intent_list = get_task_from_query(queryStr)
    if len(intent_list) == 0:
        return {'status': 'ok', 'output': ['magic']}
    return {'status': 'ok', 'output': intent_list}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
