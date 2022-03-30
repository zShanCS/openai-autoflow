import argparse

import torch
from sentence_transformers import SentenceTransformer, util

task2prompt = {
    'code2nl': ["What does this code do?", "Explain this piece of code", "Explain what this function is doing", "Explanation of the above in human readable format"],
    'fix_bugs': ["Fix bugs in this code", "Solve the issues and/or errors in the above code", "Propose a solution for the bugs in this code"],
    'get_api_request_code': ["Send an API Request", "Fetch data from an API", "Use an API to do something"],
    'get_error_explanation': ["Explain why the above code doesn't work", "Run diagnostics for the above code", "Why doesn't this code work", "Check this code for issues like bugs"],
    'nl2sql': ["Generate an SQL Query to do this", "Write a query to perform this task", "Write SQL that does this"],
    'sql2nl': ["Explain the following SQL Query", "Write documentation for this SQL", "Tell me what does query does"],
    'code2docstring': ["Write documentation for this code", "Document the provided code", "Write a docstring for this function"],
    'get_oneliner': ["Convert and rewrite this function to one line of code", "Write a oneliner for a function", "Do this in one line only"],
    'code2ut': ["Write unit tests for this code", "Generate assertions for this function", "Write a set of assert statements or tests for this code"],
    'complete_code': ["Complete an incomplete portion of code", "Fill up what's left for this code", "Generate the remaining portion", "Write what's left"]
}

prompt2task = {
    prompt: task for task in task2prompt for prompt in task2prompt[task]}
# Corpus with example sentences
corpus = list(prompt2task.keys())

device = torch.device(
    'cuda') if torch.cuda.is_available() else torch.device('cpu')
embedder = SentenceTransformer('all-MiniLM-L6-v2').to(device)
corpus_embeddings = torch.load('intent_embeddings.pt', device)


def get_most_similar(query, corpus_embeddings, top_k):
    '''
    Get the embeddings in the corpus that are most similar to
    the query string
    '''
    with torch.no_grad():
        query_embedding = embedder.encode(
            query, convert_to_tensor=True).to(device)
    # Find the closest top_k sentences of the corpus for each query sentence based on cosine similarity
    hits = util.semantic_search(
        query_embedding, corpus_embeddings, top_k=top_k)
    # free gpu memory
    torch.cuda.empty_cache()
    # Get the hits for the first query
    hits = hits[0]
    return hits


def filter_hits(hits, threshold):
    '''Keep only those hits that are >= threshold'''
    new_hits = []
    for hit in hits:
        if hit['score'] >= threshold:
            new_hits.append(hit)
    return new_hits


def get_task_from_hits(hits, corpus):
    '''Get the corresponding tasks from the most similar hits'''
    tasks = set()
    for hit in hits:
        corpus_id = hit['corpus_id']
        prompt = corpus[corpus_id]
        task = prompt2task[prompt]
        tasks.add(task)
    return list(tasks)


def get_task_from_query(query, top_k=3, threshold=0.5):
    '''
    Pass a query string
    Get a list of the tasks that may have been intended in the query
    '''
    global corpus_embeddings
    global corpus
    hits = get_most_similar(query, corpus_embeddings, top_k)
    hits_above_thresh = filter_hits(hits, threshold)
    list_of_tasks = get_task_from_hits(hits_above_thresh, corpus)
    return list_of_tasks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the task(s) for a query')
    parser.add_argument('query', type=str, help='the query string')
    args = parser.parse_args()
    tasks = get_task_from_query(args.query)
    print(tasks)
