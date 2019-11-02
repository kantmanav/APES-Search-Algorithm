
from settings import es


def execute(request_obj, nlp_libs=None, *args, **kwargs):
    task = request_obj.get('task', 'search')
    data = request_obj.get('data', list())
    resp = str()
    if task == 'search':
        for obj in data:
            question = nlp_libs(obj.get('question', '')) 
            es_index = obj.get('index', 'chapter5')
            content, search_ents_txt = get_entities_from_question(question)
            doc_hits = get_pars_with_entities(elastic_index=es_index, content=content)
            poss_pars = [nlp_libs(doc['_source']['content']) for doc in doc_hits]
            prox_scores = get_prox_scores(search_ents_txt, question, poss_pars) 
            best_hit = prox_scores.index(min(prox_scores))
            best_par = doc_hits[best_hit]
            resp = best_par
    #TODO
    if task == 'something else':
        resp = ''

    return resp

#returns list of important entities (tokens)
def get_search_ents(spacy_doc):
    search_ents = []
    for token in spacy_doc:
        if token.pos_ == 'NOUN' or token.pos_ == 'ADJ':
            search_ents.append(token)
    return search_ents

#returns string w/ important entities in question (correct format for search)
def get_entities_from_question(spacy_doc):
    content = str()
    search_ents = get_search_ents(spacy_doc)
    search_ents_txt = [token.text for token in search_ents]
    content = ' '.join(search_ents_txt)
    return content, search_ents_txt

#returns list of paragraphs (documents) containing the relevant entities (in content)
def get_pars_with_entities(elastic_index=None, content=None):
    body = { 'query': { 'bool': { 'must': [{ 'match': { 'content': content }}]}}}
    res = es.search(index=elastic_index, body=body)
    doc_hits = res['hits']['hits']
    return doc_hits





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
     prox_score = float(dist_sum) / float(len(ent_pos_list))
     return prox_score
 
def get_prox_scores(search_ents_txt, spacy_doc, pars):
    prox_scores = []
    search_ents = get_search_ents(spacy_doc)
    for par in pars:
        ent_positions = []
        for i in range(len(search_ents)):
            ent_positions.append([token.i for token in par if token.text == search_ents_txt[i]])
        prox_scores.append(prox_sc(ent_positions))
    return prox_scores

#s = 'What is the change in the genetic composition of a population over time?'
#question = nlp(s)



#res = es.search(index='chapter5', body=)

# doc_hits = res['hits']['hits']
# pars = [nlp(doc['_source']['content']) for doc in res['hits']['hits']]
#
#
# def minimum_dist(a, b):
#     if len(a) == 0 or len(b) == 0:
#         return 100
#     a_idx = 0
#     b_idx = 0
#     dist = abs(a[0] - b[0])
#     while (a_idx < len(a) and b_idx < len(b)):
#         if abs(a[a_idx] - b[b_idx]) < dist:
#             dist = abs(a[a_idx] - b[b_idx])
#         if a[a_idx] < b[b_idx]:
#             a_idx += 1
#         else:
#             b_idx += 1
#     return dist
#
#
# def prox_sc(ent_pos_list):
#     dist_sum = 0
#     for i in range(len(ent_pos_list) - 1):
#         for k in range(i + 1, len(ent_pos_list)):
#             dist_sum += minimum_dist(ent_pos_list[i], ent_pos_list[k])
#     dist_avg = float(dist_sum) / float(len(ent_pos_list))
#     return dist_avg
#
#
# prox_scores = []
# for par in pars:
#     ent_positions = []
#     for i in range(len(search_ents)):
#         ent_positions.append([token.i for token in par if token.text == search_ents_txt[i]])
#     prox_scores.append(prox_sc(ent_positions))
#
# # Will implement function to standardize proximity scores in the future
#
# best_hit = prox_scores.index(min(prox_scores))
# best_par = doc_hits[best_hit]
#
# print(best_par)