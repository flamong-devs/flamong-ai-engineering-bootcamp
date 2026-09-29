import unittest
from bootcamp.core import *
from bootcamp.llm import agent,chat
from unittest.mock import patch
class CoreTests(unittest.TestCase):
 def test_split_counts(self): self.assertEqual(audit(),{'train':36,'dev':12,'test':12})
 def test_heldout_vocab(self):
  m=NaiveBayes().fit(tickets('train'));self.assertNotIn('remittance',m.vocab)
 def test_classification_smoke(self): self.assertEqual(NaiveBayes().fit(tickets('train')).predict('my debit card was lost'),'card')
 def test_archive_excluded(self):self.assertNotIn('P00',[x['id'] for x in Retriever().search('all pending transfers complete five minutes',k=10)])
 def test_acl(self):self.assertNotIn('R01',[x['id'] for x in Retriever().search('internal risk review',role='customer',k=10)])
 def test_risk_role(self):self.assertIn('R01',[x['id'] for x in Retriever().search('internal risk review',role='risk')])
 def test_zero_vector(self):self.assertEqual(Retriever().search('zzzyyyxxx'),[])
 def test_unknown_citation(self):
  with self.assertRaises(ValueError):validate_answer({'answer':'text','citations':['FAKE'],'abstain':False},['P01'])
 def test_uncited_claim(self):
  with self.assertRaises(ValueError):validate_answer({'answer':'text','citations':[],'abstain':False},['P01'])
 def test_valid_abstention(self):self.assertTrue(validate_answer({'answer':'I cannot verify','citations':[],'abstain':True},[])['abstain'])
 def test_owner_boundary(self):
  with self.assertRaises(PermissionError):get_transaction('TX200','learner_a')
 def test_read_own(self):self.assertEqual(get_transaction('TX100','learner_a')['status'],'pending')
 def test_actor_injection(self):
  with self.assertRaises(ValueError):execute_tool('get_transaction',{'transaction_id':'TX200','actor':'learner_b'},'learner_a','support')
 def test_unknown_tool(self):
  with self.assertRaises(ValueError):execute_tool('send_money',{'amount':100},'learner_a','support')
 def test_loop_repeat(self):
  r=agent('status',planner=lambda _: {'tool':'search','args':{'query':'pending transfer'}})
  self.assertEqual(r['stopped'],'repeat')
 def test_budget(self):
  count=iter(range(20))
  r=agent('status',max_steps=2,planner=lambda _: {'tool':'search','args':{'query':'pending '+str(next(count))}})
  self.assertEqual(r['stopped'],'budget');self.assertEqual(len(r['trace']),2)
 def test_trace(self):
  actions=iter([{'tool':'get_transaction','args':{'transaction_id':'TX100'}},{'final':'TX100 is pending in the fixture.'}])
  r=agent('TX100',planner=lambda _:next(actions));self.assertEqual(r['trace'][0]['observation']['status'],'pending')
 def test_gradient(self):
  r=math_demo();self.assertAlmostEqual(r['updated_weight'],1.3);self.assertLess(r['new_loss'],r['loss'])
 def test_mock_ollama_protocol(self):
  class Response:
   def __enter__(self):return self
   def __exit__(self,*_):pass
   def read(self):return json.dumps({'done':True,'message':{'content':'{"answer":"ok"}'}}).encode()
  with patch('urllib.request.urlopen',return_value=Response()) as call:
   self.assertEqual(chat([{'role':'user','content':'hello'}],model='test-model'),{'answer':'ok'})
   self.assertEqual(call.call_args.args[0].full_url,'http://127.0.0.1:11434/api/chat')
if __name__=='__main__':unittest.main()
