import argparse,json,sys
from .core import audit,classifier_report,Retriever,evidence_preview,retrieval_report,bigram_demo,math_demo,get_transaction
from .llm import ask,agent
p=argparse.ArgumentParser(description='Flamong AI Engineering Bootcamp. Synthetic data only.')
p.add_argument('command',choices=['audit','classify','math','bigram','search','ask','evaluate','transaction','agent'])
p.add_argument('text',nargs='?',default='How should we handle a pending transfer?')
p.add_argument('--split',choices=['dev','test'],default='dev')
p.add_argument('--mode',choices=['extractive','ollama'],default='extractive')
p.add_argument('--k',type=int,default=3)
p.add_argument('--role',choices=['support','customer','risk'],default='support')
p.add_argument('--actor',default='learner_a',help='Toy session fixture, not authentication')
a=p.parse_args()
try:
 if not 1<=a.k<=10:raise ValueError('k must be 1..10')
 if a.command=='audit':r=audit()
 elif a.command=='classify':r=classifier_report(a.split)
 elif a.command=='math':r=math_demo()
 elif a.command=='bigram':r=bigram_demo()
 elif a.command=='search':r=Retriever().search(a.text,a.role,a.k)
 elif a.command=='evaluate':r=retrieval_report(a.split,a.k)
 elif a.command=='transaction':r=get_transaction(a.text,a.actor)
 elif a.command=='agent':
  if a.mode!='ollama':raise ValueError('agent requires --mode ollama and an installed local model; see tests for a scripted loop')
  r=agent(a.text,actor=a.actor,role=a.role)
 else:r=ask(a.text,a.role) if a.mode=='ollama' else evidence_preview(a.text,a.role,a.k)
 print(json.dumps(r,indent=2,ensure_ascii=False))
except Exception as e:
 print(f'{type(e).__name__}: {e}',file=sys.stderr);sys.exit(1)
