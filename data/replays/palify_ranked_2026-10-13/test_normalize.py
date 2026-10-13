import copy,json,unittest
from fetch import ROOT,get
from collect import history,PrivateHistory,cache_ref
from normalize import cached,result_evidence,deck_record
from archetypes import classify
MID='8b089df8-e4f7-4d85-9f72-ca4dc953ff0f'
class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Fixtures are real already-cached pilot responses; never fetch in tests.
        cls.r=cached(cache_ref('https://palify.org/api/pvp/match/'+MID+'/replay'))
        cls.d=cached(cache_ref('https://palify.org/api/pvp/match/'+MID+'/decks'))
        import gzip
        cls.public=gzip.decompress((ROOT/cache_ref('https://palify.org/u/keitosato2015')['cache_body']).read_bytes()).decode()
        cls.private=gzip.decompress((ROOT/cache_ref('https://palify.org/u/zendaman3gou')['cache_body']).read_bytes()).decode()
    def test_profile_parser_real(self):self.assertEqual(len(history(self.public)),20)
    def test_private_profile_not_probed(self):
        with self.assertRaises(PrivateHistory):history(self.private)
    def test_replay_over_conflicting_profile(self):
        g=next(g for g in history(self.public) if g['id']==MID)
        e=result_evidence(self.r,[{'handle':'keitosato2015','history':g}])
        self.assertEqual(e['first_player']['side'],'p2');self.assertEqual(e['winner']['side'],'p1')
        self.assertIn('profile_first_player_disagrees_with_replay',e['quality_flags'])
        self.assertNotIn('profile_winner_disagrees_with_replay',e['quality_flags'])
    def test_actual_replay_turn_counter_repeats_for_other_player(self):
        r=cached(cache_ref('https://palify.org/api/pvp/match/73bd7a3a-d366-4842-a5a7-eddcf178bdd1/replay'))
        e=result_evidence(r,[])
        self.assertEqual(e['first_player']['side'],'p2')
        self.assertNotIn('replay_first_player_conflict',e['quality_flags'])
    def test_no_first_turn_no_guess(self):
        r=copy.deepcopy(self.r)
        for f in r['frames']:f['view']['setup']=None;f['view']['activeIs']=None;f['view']['log']=[]
        self.assertIsNone(result_evidence(r,[])['first_player']['side'])
    def test_conflicting_replay_abstains(self):
        r=copy.deepcopy(self.r);r['frames'][6]['view']['activeIs']='me'
        e=result_evidence(r,[]);self.assertIsNone(e['first_player']['side']);self.assertIn('replay_first_player_conflict',e['quality_flags'])
    def test_unfinished_has_no_winner(self):
        r=copy.deepcopy(self.r);r['frames'][-1]['view']['status']='active'
        self.assertIsNone(result_evidence(r,[])['winner']['side'])
    def test_actual_full_decks(self):
        for s in ('p1','p2'):
            d=deck_record(self.d[s]);self.assertEqual(d['main_total'],50);self.assertIsNone(d['soul_counts']);self.assertEqual(d['archetype']['source'],'inferred')
    def test_invalid_sequence_flagged(self):
        r=copy.deepcopy(self.r);r['frames'][1]['seq']=0
        self.assertIn('frame_sequence_invalid',result_evidence(r,[])['quality_flags'])
if __name__=='__main__':unittest.main()
