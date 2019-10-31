# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host':'localhost','port':9200}])

import spacy
nlp = spacy.load('en_core_web_sm')

s = 'What is the change in the genetic composition of a population over time?'
question = nlp(s)

search_ents = []
for token in question:
    if token.pos_ == 'NOUN' or token.pos_ == 'ADJ':
        search_ents.append(token)
        
#Will implement entity list in the future
        
search_ents_txt = [token.text for token in search_ents]
content = ' '.join(search_ents_txt)
        
res = es.search(index = 'chapter5', body = {
    'query': {
        'bool': {
            'must': [{
                'match': {
                    'content': content
                }
            }]
        }
    }
})

doc_hits = res['hits']['hits']
pars = [nlp(doc['_source']['content']) for doc in res['hits']['hits']]

def minimum_dist(a, b):
    if len(a) == 0 or len(b) == 0:
        return 100
    a_idx = 0
    b_idx = 0
    dist = abs(a[0] - b[0])
    while (a_idx < len(a) and b_idx < len(b)):
        if abs(a[a_idx] - b[b_idx]) < dist:
            dist = abs(a[a_idx] - b[b_idx])
        if a[a_idx] < b[b_idx]:
            a_idx += 1
        else:
            b_idx += 1
    return dist

def prox_sc(ent_pos_list):
    dist_sum = 0
    for i in range(len(ent_pos_list) - 1):
        for k in range(i + 1, len(ent_pos_list)):
            dist_sum += minimum_dist(ent_pos_list[i], ent_pos_list[k])
    dist_avg = float(dist_sum) / float(len(ent_pos_list))
    return dist_avg

prox_scores = []
for par in pars:
    ent_positions = []
    for i in range(len(search_ents)):
        ent_positions.append([token.i for token in par if token.text == search_ents_txt[i]])
    prox_scores.append(prox_sc(ent_positions))
    
#Will implement function to standardize proximity scores in the future
    
best_hit = prox_scores.index(min(prox_scores))
best_par = doc_hits[best_hit]

print(best_par)