import argparse
import itertools
import os
import pickle
import re

import torch
from sentence_transformers.util import semantic_search
from transformers import RobertaModel, RobertaTokenizer

weights = '/content/drive/MyDrive/devrev'
device = torch.device(
    'cuda') if torch.cuda.is_available() else torch.device('cpu')
search_tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
search_model = RobertaModel.from_pretrained(weights).to(device)

def create_embeddings(input_json, seq_length):
    '''Create code embeddings for user code base'''
    segments = {}
    # First, take as input a json of programs and file paths
    for program in input_json:
        fp = program['fp']
        content = program['content']
        # Tokenize the content of each program
        tokens = search_tokenizer.encode(content)
        # initial 256 tokens
        segments[fp] = [tokens[:seq_length]]
        # break the tokens into lists of 256 max length
        for seg_num in range(seq_length, len(tokens), seq_length - 1):
            # [0] is CLS
            tokens_segment = [0] + tokens[seg_num:seg_num + seq_length - 1]
            # for each program, store a list of lists of tokens
            segments[fp].append(tokens_segment)
    # get every code segment tokens list from every file and flatten it
    all_code_segments_2d = list(itertools.chain(*segments.values()))
    code_embeddings = None
    for code_tokens in all_code_segments_2d:
        # create tensor from tokens
        code_tensor = torch.tensor(code_tokens).unsqueeze(0).to(device)
        # create embedding from tensor
        with torch.no_grad():
            code_vec = search_model(code_tensor)[1].to(device)
        # first tensor
        if code_embeddings == None:
            code_embeddings = code_vec
            # concatenate with all embeddings
        else:
            code_embeddings = torch.cat((code_embeddings, code_vec), 0)
    torch.save(code_embeddings, "code_embeddings.pt")
    # save tokenized.pkl
    with open("all_code_segments.pkl", "wb") as f:
        pickle.dump(all_code_segments_2d, f)
    # free memory
    del code_embeddings
    del segments
    del all_code_segments_2d
    torch.cuda.empty_cache()

def get_most_similar(query, top_k):
    '''
    Get the embeddings in the code embedddings
    that are most similar to the query string
    '''
    code_embeddings = torch.load("./code_embeddings.pt", map_location=device)
    global search_model
    query_tokens = search_tokenizer.encode(
        query, return_tensors="pt").to(device)
    query_embedding = search_model(query_tokens)[1]
    # Find the closest top_k sentences of the corpus for each query sentence based on cosine similarity
    hits = semantic_search(query_embedding, code_embeddings, top_k=top_k)
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

def remove_special_tokens(string):
    return re.sub(r'<\S+>', '', string)


def get_code_from_hits(hits):
    '''Get the corresponding code from the most similar hit(s)'''
    global search_tokenizer
    code_and_filepaths = list()
    # just get the first one
    hit = hits[0]
    # the index inside the corpus
    code_segment_index = hit['corpus_id']
    # get the list of all code segments
    with open("all_code_segments.pkl", "rb") as f:
        all_code_segments = pickle.load(f)
    # the tokens list for this code segment
    code_segment_tokens = all_code_segments[code_segment_index]
    # free memory
    del all_code_segments
    # the original code segment
    code_segment = search_tokenizer.decode(code_segment_tokens)
    # remove special tokens
    code_segment = remove_special_tokens(code_segment)
    return code_segment


def search_for_code(query, top_k=1, threshold=0.4, input_json=None):
    '''
    Pass a query string
    Return a JSON array with intended code and its filepath
    '''
    # Create embeddings if they don't exist
    global search_tokenizer
    if not os.path.exists("./code_embeddings.pt"):
        if input_json != None:
            create_embeddings(input_json, seq_length=search_tokenizer.model_max_length)
        else:
            print("ERROR: EMBEDDINGS DO NOT EXIST")
            return ''
    hits = get_most_similar(query, top_k)
    hits_above_thresh = filter_hits(hits, threshold)
    code_segment = get_code_from_hits(hits_above_thresh)
    return code_segment
