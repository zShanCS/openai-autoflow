# -*- coding: utf-8 -*-

import inspect
import json
import re

from code_gen import get_code


def get_comment(language, ml=True):
    '''Get the comment symbol for the specified programming language'''
    if language.lower() == 'python':
        if ml:
            return ('"""', '"""')
        else:
            return '#'
    else:
        if ml:
            return ('/*', '*/')
        else:
            return '//'


"""API Call

```
'''
Send a request to the <API_Name> API to <task> using the following parameters: 
<params_dict>
Use the following API token header: <token>
'''
```

**Stop**


*   '''
*   \n\n

**Parameters**
*   temperature=0
*   presence_penalty & frequency_penalty = 0.5
*   max_tokens=128

### Optimal Parameters for this template
"""


def get_api_template(api_name, task, params, token=None):
    template = f'"""\n'
    template += f'Send a request to the {api_name} API to {task} using the following parameters:\n'
    if type(params) != str:
        params = json.dumps(params)
    template += params + "\n"
    if token:
        template += f"Use the following API token header: {token}\n"
    template += '"""'
    return template


def get_api_request_code(api_name, task, params, token=None):
    prompt = get_api_template(api_name, task, params, token)
    code = get_code(prompt, max_tokens=128, temperature=0.2,
                    presence_penalty=0.5, frequency_penalty=0.5,
                    stop=['"""', '\n\n\n'], best_of=3)
    return code


"""SQL Queries

### SQL Explanation

**Explanation**

```
<query>
-- Explanation of the above query in human readable format
--
```

**Stopwords**

- #
- \n\n
- SELECT
- '''


**Parameters**
- max_tokens = 256
- temperature = 0.4
"""


def get_sql_explanation_template(query):
    template = """<query>
    -- Explanation of the above query in human readable format
    --"""
    template = inspect.cleandoc(template)
    # preprocess the query
    query = query.strip()
    query = inspect.cleandoc(query)
    template = re.sub(r"<query>", query, template)
    return template


def sql2nl(query):
    query = get_sql_explanation_template(query)
    explanation = get_code(query, max_tokens=256, temperature=0.4,
                           stop=["#", "\n\n", "SELECT", '"""'])
    explanation = "--" + explanation
    # remove lines without --
    explanation_split = explanation.split('\n')
    new_explanation = []
    # to prevent duplicates
    new_explanation_set = set()
    for line in explanation_split:
        if line.startswith('--') and line not in new_explanation_set:
            new_explanation.append(line)
            new_explanation_set.add(line)
        else:
            break
    explanation = "\n".join(new_explanation)
    return explanation


"""### SQL Generation

**Stopwords**

- #
- \-\-
- ;
- '''

```
'''
Table <table name>, columns = <list of columns>
.
.
.

Create a <SQL Engine> query to <task>
'''
```
"""


def get_sql_generation_template(table_names, col_names, task, sql_engine="MySQL"):
    if len(table_names) < 1:
        print("ERROR: table_names must contain atleast one table")
        return ''
    if len(table_names) != len(col_names):
        print("ERROR: len(table_names) must equal len(col_names)")
        return ''
    template = '"""\n'
    # preprocess the query
    for i in range(len(table_names)):
        tb_name = table_names[i]
        cols = col_names[i]
        template += f'Table {tb_name}, columns = {cols}\n'
    template += f'\nCreate a {sql_engine} query to {task}\n'
    template += '"""\nSELECT'
    return template


def nl2sql(table_names, col_names, task, sql_engine="MySQL"):
    template = get_sql_generation_template(
        table_names, col_names, task, sql_engine)
    sql = get_code(template, max_tokens=256, temperature=0.2,
                   stop=['#', '\n\n', ';', '"""'], best_of=3)
    sql = "SELECT" + sql
    return sql


"""## Code to Natural Language Explanation (Except SQL)

**Explanation**

```
<Natural Language statement>
<Code to be explained>
-- <Natural Language Statement indicating start of explanation>
```

**Stopwords**

- \<multline_ending_comment_symbol>

*e.g. Python= ''', C/C++/Java = */, HTML = -->, etc.*



**Parameters**
- temperature=0.3,
- max_tokens = 100,
- frequency_penalty=0.2

#### Recommendations:

##### 1. If code is a function, the function header should have a meaningful name

##### 2. Test cases and comments can be provided for more accurate description

##### 3. Simple and refactored codes produce better explanation than complex ones

#### **prompt** :

```
'''<comment start> Code excerpt and explanation.<comment end>
<comment start>Excerpt:
<code><comment end>

<comment start>Explanation:
'''
```
"""


def get_code2nl_template(code, language):
    prompt = '''<comment start> Code excerpt and explanation.<comment end>
    <comment start>Excerpt:
    <code><comment end>

    <comment start>Explanation:
    '''
    prompt = inspect.cleandoc(prompt)
    ml_comment = get_comment(language)
    prompt = re.sub("<comment start>", ml_comment[0], prompt)
    prompt = re.sub("<comment end>", ml_comment[1], prompt)
    prompt = re.sub("<code>", code, prompt)

    return prompt


def code2nl(code, language):
    prompt = get_code2nl_template(code, language)
    return get_code(prompt, temperature=0.3, max_tokens=2048, frequency_penalty=0.2, stop=['"""', '*/'])


"""Bug Fixing

*   [Can OpenAI Codex Debug Its Own Code?](https://www.youtube.com/watch?v=Pkp1MRFGUVo)
*   [Automatic Program Repair with OpenAI’s Codex
](https://arxiv.org/pdf/2111.03922.pdf)

### Error Explanation

```
<function>

'''The function above does not work as intended.
The following corrections are needed:
1.
```
"""


def get_error_explanation_template(function):
    template = function + "\n\n"
    template += '"""The function above does not work as intended.\n'
    template += 'The following corrections are needed:\n1.'
    return template


def get_error_explanation(function):
    prompt = get_error_explanation_template(function)
    code = get_code(prompt, temperature=0.2, stop=['#', '"""', '//', '/*'],
                    max_tokens=256, frequency_penalty=1, best_of=5)
    return code


"""Fix Bugs in Functions

```
<cmtStart> Fix bugs in the following function <cmtEnd>
<funcHeader>
<funcBody>

<cmtStart> Fixed function <cmtEnd>
<funcHeader>
```
It is recommended that the function has a docstring
"""


def get_fix_bugs_template(function, language):
    function = function.strip()
    parts = function.split('\n')
    header = parts[0]
    body = parts[1:]
    docstring = None
    if '"""' in body[0]:
        docstring = body[0] + '\n'
        i = 1
        while '"""' not in body[i]:
            docstring += body[i] + '\n'
            i += 1
        docstring += body[i] + '\n'
    cmt_start, cmt_end = get_comment(language)

    template = f'{cmt_start} Fix bugs in the below function {cmt_end}\n'
    template += function + "\n\n"
    template += f'{cmt_start} Fixed function {cmt_end}\n'
    template += header
    if docstring:
        template += f"\n{docstring}"
    return template


def fix_bugs(function, language):
    function = function.strip()
    if 'python' in language.lower():
        stop = ['"""', '\n\n', '###']
        if '#' not in function:
            stop.append('#')
        template = "# Python 3\n"
    else:
        stop = ['#', '"""', '/*']
        if '//' not in function:
            stop.append('//')
        template = f'# {language}\n'
    template = get_fix_bugs_template(function, language)
    temperature = 0
    code = get_code(template, max_tokens=512, frequency_penalty=0.4,
                    temperature=temperature, stop=stop, best_of=3)
    while code.strip() == '':
        temperature += 0.1
        code = get_code(template, max_tokens=512, frequency_penalty=0.4,
                        temperature=temperature, stop=stop, best_of=3)
    return code


"""## Write Comments/Docstring for Code

**Explanation**

```
<Function>
<Natural language statement indicating start of a docstring>
-- <Generated docstring>
```

**Stopwords**

- \"\"\" (ending mult-line comment symbol of Python)
- #

**Parameters**
- temperature = 0.20,
- max_tokens = 150,
- frequency_penalty = 0.50

#### **prompt** :

```
'''<code>
# Summary of above function with an elaborate, high quality docstring:
'''
```
"""


def get_code2docstring_template(code):
    prompt = '''<code>
    # Summary of above function with an elaborate, high quality docstring:
    """'''
    prompt = inspect.cleandoc(prompt)
    return re.sub("<code>", code, prompt)


def code2docstring(code):
    prompt = get_code2docstring_template(code)
    code = get_code(prompt, temperature=0.2, max_tokens=150,
                    frequency_penalty=0.5, stop=['"""'])
    return code


"""Code Oneliners

### Template

**Explanation**

```
<Set of Natural Language statements>
<Incomplete code: Function Header>
-- <One line function completed>
```

**Stopwords**

- \n
- \<comment_symbols>
- \<print_statements>


**Parameters**
- temperature=0.1,
- max_tokens = 40,
- frequency_penalty=1,
- presence_penalty=1,


#### **prompt** :

```
'''<comment start> Convert this function in <language> to a one line function<comment end>
<function header>
    <code>

<comment start><language> one line version<comment end>:

<function header>
    <return statement>'''
```
"""


def get_oneliner_template(function_code, language):
    prompt = '''<comment start> Convert this function in <language> to a one line function<comment end>
    <function header>
        <code>

    <comment start> <language> one line version<comment end>:
    <function header>
        <return statement>'''
    prompt = inspect.cleandoc(prompt)
    prompt = re.sub("<comment start>", get_comment(language)[0], prompt)
    prompt = re.sub("<comment end>", get_comment(language)[1], prompt)
    prompt = re.sub("<language>", language, prompt)
    prompt = re.sub("<function header>", function_code.split('\n')[0], prompt)
    prompt = re.sub(
        "<code>", function_code[function_code.find('\n')+1:], prompt)
    prompt = re.sub("<return statement>", 'return', prompt)

    return prompt


def get_oneliner(function_code, language):
    prompt = get_oneliner_template(function_code, language)
    code = get_code(prompt, temperature=0.2, max_tokens=150,
                    frequency_penalty=0.5, stop=['"""', '\n'])
    return code


"""## Write Unit Tests for a function

```
<function header>
<function body>

<mlcomment start> Write a set of unit tests for the function <function name> <mlcomment end>

<slcomment> Unit Tests
```

**Stop**
- Comments for given language
- temperature = 0
- frequency_penalty = 0.1
- presence_penalty = 0.1
"""


def get_unit_tests_template(function, language):
    parts = function.strip().split('\n')
    header = parts[0]
    body = '\n'.join(parts[1:])
    # get name of function i.e. the word that comes before a '('
    name = header.split('(')[0].split(' ')[-1]
    template = f'{header}\n{body}\n\n'
    cmt_start, cmt_end = get_comment(language)
    template += f'{cmt_start} Write a set of unit tests for the function {name} {cmt_end}\n\n'
    sl_cmt = get_comment(language, False)
    template += f'{sl_cmt} Unit Tests'
    return template


def code2ut(function, language):
    if 'python' in language.lower():
        template = "Python 3\n"
    else:
        template = f"{language}\n"
    template += get_unit_tests_template(function, language)
    temperature = 0
    code = get_code(template, max_tokens=256, frequency_penalty=0.1, presence_penalty=0.1,
                    temperature=temperature, stop=['#', '//', '/*'], best_of=3)
    while code.strip() == '':
        temperature += .1
        code = get_code(template, max_tokens=256, frequency_penalty=0.1,
                        presence_penalty=0.1, temperature=temperature,
                        stop=['#', '"""', '//', '/*'], best_of=3)
    return code


'''
Code Completion

**Template 1**
"""Complete the following piece of code for <task>"""
<code>

**Template 2**
"""Complete the following function"""
<docstring for non-python>
<function header>
<docstring for python>
<code>?
'''


def get_code_completion_template(code, task=''):
    code_parts = code.split()
    if '/**' in code_parts[0]:
        docstring = code_parts[0] + "\n"
        i = 1
        while '*/' not in code_parts[i]:
            docstring += code_parts[i]
            i += 1
        docstring += code_parts[i] + "\n"
        function_code = code_parts[i+1:]
        template = '"""Complete the following function"""\n'
        template += docstring
        template += function_code
    else:
        if '"""' in code_parts[1] or "'''" in code_parts[1]:
            template = '"""Complete the following function"""'
            template += code
        else:
            template = f'"""Complete the following piece of code for {task}"""\n'
            template += code
    return template


def complete_code(code, task=''):
    prompt = get_code_completion_template(code, task)
    if task == '':
        print("WARNING: Task not provided. Resulting code may not be accurate")
        temperature = 0.8
    else:
        temperature = 0.2
    code = get_code(prompt, temperature=temperature, max_tokens=256, frequency_penalty=0.8,
                    presence_penalty=0.4, stop=['\n\n\n', '"""'])
    return code


def send_code_request(task, **kwargs):
    tasks = {
        'api': get_api_request_code,
        'sql2nl': sql2nl,
        'nl2sql': nl2sql,
        'code2nl': code2nl,
        'error_explain': get_error_explanation, 
        'fixbugs': fix_bugs,
        'code2doc': code2docstring,
        'oneliner': get_oneliner,
        'ut': code2ut,
        'complete': complete_code,
    }
    if task in tasks:
        return tasks[task](**kwargs)
    else:
        print('WARNING: Task does not exist! Using prompt as input to Codex')
        return get_code(task, temperature=0.6, frequency_penalty=0.8, presence_penalty=0.4,
                        max_tokens=512, stop=['\n\n\n'])
