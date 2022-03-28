from typing import Optional
from pydantic import BaseModel

class Prompt(BaseModel):
    prompt:str
class Prompt_Language(BaseModel):
    prompt:str
    language:str

class Code_Task(BaseModel):
    code:str
    task:str

class API_Req(BaseModel):
    api_name:str
    task:str
    params:str
    token: Optional[str]
class IntentAnalysis(BaseModel):
    query:str

class QueryInfo(BaseModel):
    task:str
    tableName:str
    columnName:str