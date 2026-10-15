"""Creates SYNTHETIC TEST PRICES, NEVER for fund performance or actual research conclusions."""
import csv, random, math
from datetime import date,timedelta
from pathlib import Path
random.seed(4115)
start=date(2020,1,2);end=date(2025,12,31)
prices={'SPY':100.,'IEF':100.,'GLD':100.,'UUP':100.}
path=Path(__file__).resolve().parents[1]/'data'/'SYNTHETIC_TEST_ONLY_prices.csv'
rows=[];d=start
while d<=end:
    if d.weekday()<5:
        for t,p in prices.items():
            daily={'SPY':.0003,'IEF':.00007,'GLD':.00012,'UUP':.00004}[t]
            sigma={'SPY':.011,'IEF':.004,'GLD':.009,'UUP':.004}[t]
            prices[t]=p*math.exp(daily+sigma*random.gauss(0,1))
            rows.append([d.isoformat(),t,round(prices[t],8)])
    d+=timedelta(days=1)
with path.open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['date','ticker','adj_close']);w.writerows(rows)
print('SYNTHETIC TEST DATA ONLY:',path,len(rows),'rows')
