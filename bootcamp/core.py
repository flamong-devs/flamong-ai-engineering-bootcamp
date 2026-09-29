"""Readable baselines. Standard library only; not production fintech software."""
from collections import Counter, defaultdict
from pathlib import Path
import json, math, re, random
ROOT = Path(__file__).resolve().parents[1]
STOP = set('a an and are as at be by can do for from how i in is it me my of on or the to was what when why with you your'.split())
def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]
def load(name):
    return json.loads((ROOT / 'data' / name).read_text())
def tickets(split):
    return [json.loads(s) for s in (ROOT/'data/tickets.jsonl').read_text().splitlines()
            if json.loads(s)['split'] == split]
def audit():
    seen, groups, counts = set(), {}, Counter()
    for split in ('train', 'dev', 'test'):
        for r in tickets(split):
            canonical=' '.join(tokens(r['text']))
            if canonical in seen: raise ValueError('Duplicate normalized ticket')
            seen.add(canonical)
            if r['group'] in groups and groups[r['group']] != split:
                raise ValueError('Group crosses splits')
            groups[r['group']] = split
            if r['label'] not in ('transfer','card','access'):raise ValueError('Bad label')
            counts[split] += 1
    return dict(counts)
class NaiveBayes:
    """Multinomial NB with add-one smoothing; fit on train only."""
    def fit(self, rows):
        self.doc_counts=Counter(r['label'] for r in rows)
        self.words=defaultdict(Counter);self.vocab=set()
        for r in rows:
            ts=tokens(r['text']); self.words[r['label']].update(ts);self.vocab.update(ts)
        self.n=len(rows);self.totals={k:sum(v.values()) for k,v in self.words.items()}
        return self
    def predict(self, text):
        scores={}
        for k,n in self.doc_counts.items():
            score=math.log(n/self.n)
            for t in tokens(text):
                if t in self.vocab:
                    score += math.log((self.words[k][t]+1)/(self.totals[k]+len(self.vocab)))
            scores[k]=score
        return max(scores,key=scores.get)
def classifier_report(split='dev'):
    model=NaiveBayes().fit(tickets('train'));rows=tickets(split)
    labels=sorted(model.doc_counts);matrix={y:{p:0 for p in labels} for y in labels}
    errors=[]
    for r in rows:
        pred=model.predict(r['text']);matrix[r['label']][pred]+=1
        if pred!=r['label']:errors.append({'id':r['id'],'text':r['text'],'gold':r['label'],'pred':pred})
    metrics={}
    for k in labels:
        tp=matrix[k][k];fp=sum(matrix[g][k] for g in labels if g!=k);fn=sum(matrix[k][p] for p in labels if p!=k)
        prec=tp/(tp+fp) if tp+fp else 0;rec=tp/(tp+fn) if tp+fn else 0
        metrics[k]={'precision':round(prec,3),'recall':round(rec,3),'f1':round(2*prec*rec/(prec+rec),3) if prec+rec else 0}
    return {'split':split,'n':len(rows),'accuracy':round(sum(matrix[k][k] for k in labels)/len(rows),3),
            'majority_baseline':round(max(Counter(r['label'] for r in rows).values())/len(rows),3),
            'confusion_rows_gold_cols_pred':matrix,'per_class':metrics,'errors':errors,
            'caveat':'Tiny synthetic data; no claim about real support traffic.'}
class Retriever:
    def __init__(self, documents=None):
        self.docs=documents if documents is not None else load('knowledge.json')
        df=Counter()
        for d in self.docs:df.update(set(tokens(d['title']+' '+d['text'])))
        self.idf={t:math.log((1+len(self.docs))/(1+n))+1 for t,n in df.items()}
        self.vectors={d['id']:self.vector(d['title']+' '+d['text']) for d in self.docs}
    def vector(self,text):
        v={t:n*self.idf[t] for t,n in Counter(tokens(text)).items() if t in self.idf}
        norm=math.sqrt(sum(x*x for x in v.values()))
        return {t:x/norm for t,x in v.items()} if norm else {}
    def search(self,query,role='support',k=3,min_score=.05):
        q=self.vector(query);hits=[]
        for d in self.docs:
            if d['status']!='current' or role not in d['roles']:continue
            score=sum(x*self.vectors[d['id']].get(t,0) for t,x in q.items())
            if score>=min_score:hits.append({**d,'score':round(score,5)})
        return sorted(hits,key=lambda h:(-h['score'],h['id']))[:k]
def evidence_preview(query,role='support',k=3):
    hits=Retriever().search(query,role,k)
    return {'mode':'extractive evidence preview (no LLM)',
            'answer':'\n'.join(f"[{d['id']}] {d['text']}" for d in hits) if hits else 'No matching evidence. Escalate or clarify.',
            'citations':[d['id'] for d in hits]}
def validate_answer(obj,allowed):
    if not isinstance(obj,dict) or set(obj)!= {'answer','citations','abstain'}:raise ValueError('Expected answer, citations, abstain')
    if not isinstance(obj['answer'],str) or not obj['answer'].strip():raise ValueError('Empty answer')
    if type(obj['abstain']) is not bool:raise ValueError('abstain must be boolean')
    if not isinstance(obj['citations'],list) or any(type(x) is not str for x in obj['citations']):raise ValueError('citations must be string list')
    if not set(obj['citations'])<=set(allowed):raise ValueError('Unknown citation')
    if not obj['abstain'] and not obj['citations']:raise ValueError('Uncited answer')
    return obj  # ID validation does not prove claim support.
def get_transaction(transaction_id, actor):
    tx=next((r for r in load('transactions.json') if r['id']==transaction_id),None)
    if tx is None or tx['owner']!=actor:raise PermissionError('Transaction unavailable for this session')
    return {k:tx[k] for k in ('id','status','amount_kobo','as_of')}
def execute_tool(name,args,actor,role):
    if not isinstance(args,dict):raise ValueError('args must be object')
    if name=='search' and set(args)=={'query'} and isinstance(args['query'],str):
        return Retriever().search(args['query'],role)
    if name=='get_transaction' and set(args)=={'transaction_id'} and isinstance(args['transaction_id'],str):
        return get_transaction(args['transaction_id'],actor)
    raise ValueError('Unknown tool or invalid arguments')
def retrieval_report(split='dev',k=3):
    cases=[r for r in load('questions.json') if r['split']==split and r['gold_ids']]
    scores=[];fails=[]
    for r in cases:
        found={d['id'] for d in Retriever().search(r['question'],r['role'],k)}
        gold=set(r['gold_ids']);hit=bool(found&gold);scores.append((hit,len(found&gold)/len(gold)))
        if not hit:fails.append(r['id'])
    unknown=[r for r in load('questions.json') if r['split']==split and not r['gold_ids']]
    false_evidence=[r['id'] for r in unknown if Retriever().search(r['question'],r['role'],k)]
    return {'split':split,'k':k,'answerable_count':len(cases),
            'hit_at_k':sum(s[0] for s in scores)/len(scores),
            'mean_recall_at_k':sum(s[1] for s in scores)/len(scores),'misses':fails,
            'unanswerable_count':len(unknown),'unanswerable_with_hits':false_evidence,
            'note':'Retrieval scores do not measure answer quality. Unknown questions may retrieve irrelevant text.'}
def bigram_demo(seed=7):
    docs=[d['text'].lower().split() for d in load('knowledge.json') if d['status']=='current']
    following=defaultdict(Counter)
    for ts in docs:
        for a,b in zip(['<s>']+ts,ts+['</s>']):following[a][b]+=1
    rng=random.Random(seed);out=[];word='<s>'
    for _ in range(35):
        choices=following[word];word=rng.choices(list(choices),weights=list(choices.values()))[0]
        if word=='</s>':break
        out.append(word)
    return {'model':'word bigram count model; not an LLM','sample':' '.join(out)}
def math_demo():
    w=.5;x=2;y=3;prediction=w*x;loss=(prediction-y)**2;gradient=2*(prediction-y)*x;lr=.1;new_w=w-lr*gradient
    return {'dot_example':2*3+1*4,'prediction':prediction,'loss':loss,'gradient':gradient,
            'learning_rate':lr,'updated_weight':new_w,'new_loss':(new_w*x-y)**2,
            'sigmoid_2':1/(1+math.exp(-2)), 'loss_p_08':-math.log(.8)}
