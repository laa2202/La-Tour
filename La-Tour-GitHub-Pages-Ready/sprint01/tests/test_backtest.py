import tempfile, unittest, csv
from pathlib import Path
from sys import path
path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from backtest import backtest, read_prices

class TestBacktest(unittest.TestCase):
    def setUp(self):
        self.file=Path(__file__).resolve().parents[1]/'data'/'SYNTHETIC_TEST_ONLY_prices.csv'
    def test_no_lookahead_and_first_day(self):
        dates,_=read_prices(self.file)
        with tempfile.TemporaryDirectory() as tmp:
            out=backtest(self.file,Path(tmp)/'output.csv')
            self.assertEqual(out[0]['date'],dates[253].isoformat())
            self.assertTrue(all(0<=x['weight_SPY']<=.25 for x in out))
            self.assertTrue(all(x['turnover']==0 or x['date'][:7]!=out[i-1]['date'][:7] for i,x in enumerate(out) if i>0))
    def test_real_dataset_not_bundled(self):
        self.assertFalse((self.file.parent/'prices.csv').exists())

if __name__=='__main__':unittest.main()
