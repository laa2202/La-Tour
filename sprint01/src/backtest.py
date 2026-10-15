"""Common MVP evaluator: 12-month trailing signal, monthly rebalancing, long/cash, no leverage.
Inputs: date,ticker,adj_close. Calculations use signal at prior close for current-day close-to-close return.
Costs: 5 basis points per unit notional turnover. This is a teaching assumption, not an execution estimate.
"""
import csv, math, argparse
from collections import defaultdict
from datetime import date
from pathlib import Path

TICKERS=('SPY','IEF','GLD','UUP')

def read_prices(path):
    by=defaultdict(dict)
    with open(path,newline='') as f:
        rd=csv.DictReader(f)
        if rd.fieldnames!=['date','ticker','adj_close']:
            raise ValueError('Expected exact columns: date,ticker,adj_close')
        for row in rd:
            dt=date.fromisoformat(row['date']); ticker=row['ticker']; p=float(row['adj_close'])
            if ticker not in TICKERS or not math.isfinite(p) or p<=0: raise ValueError('Invalid row '+str(row))
            if ticker in by[dt]: raise ValueError('Duplicate date/ticker')
            by[dt][ticker]=p
    dates=sorted(d for d,r in by.items() if len(r)==len(TICKERS))
    if len(dates)<280: raise ValueError('Need at least 280 common trading dates')
    if any(len(by[d])!=4 for d in dates): raise ValueError('Unexpected missing values')
    return dates,by

def backtest(path,output,lookback=252, fee_bps=5):
    dates, px=read_prices(path)
    out=[]; positions={t:0.0 for t in TICKERS}; prev_signal=None
    prev_month=None
    for i in range(lookback+1,len(dates)):
        d=dates[i]; yesterday=dates[i-1]; lookback_d=dates[i-1-lookback]
        # At close yesterday, use only prices observed at or before yesterday.
        # Set target weights for the current day; rebalance only on the first trading day of each month.
        desired={t:(0.25 if px[yesterday][t]>px[lookback_d][t] else 0.0) for t in TICKERS}
        month=(d.year,d.month)
        traded=month!=prev_month
        if traded:
            turnover=sum(abs(desired[t]-positions[t]) for t in TICKERS)
            positions=desired
        else: turnover=0.0
        gross=sum(positions[t]*(px[d][t]/px[yesterday][t]-1) for t in TICKERS)
        cost=fee_bps/10000*turnover
        net=gross-cost
        bench=sum(.25*(px[d][t]/px[yesterday][t]-1) for t in TICKERS)
        out.append({'date':d.isoformat(),'net_return':net,'benchmark_return':bench,
                    'gross_return':gross,'cost':cost,'turnover':turnover,
                    **{f'weight_{t}':positions[t] for t in TICKERS}})
        prev_month=month
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=out[0]);wr.writeheader();wr.writerows(out)
    rets=[x['net_return'] for x in out]
    annual=(math.prod(1+r for r in rets)**(252/len(rets))-1) if all(1+r>0 for r in rets) else float('nan')
    mu=sum(rets)/len(rets); vol=math.sqrt(sum((r-mu)**2 for r in rets)/(len(rets)-1))*math.sqrt(252)
    sharpe=(mu*252/vol) if vol else float('nan') # assumes zero risk-free return
    wealth=1;peak=1;maxdd=0
    for r in rets:
        wealth*=1+r;peak=max(peak,wealth);maxdd=min(maxdd,wealth/peak-1)
    print(f'Days: {len(out)} | CAGR: {annual:.2%} | Ann vol: {vol:.2%} | Sharpe (rf=0): {sharpe:.2f} | MaxDD: {maxdd:.2%}')
    print(f'Output: {output} | Dataset: {path}')
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',default='results/backtest.csv');ap.add_argument('--lookback',type=int,default=252);ap.add_argument('--fee-bps',type=float,default=5)
    a=ap.parse_args();backtest(a.input,a.output,a.lookback,a.fee_bps)
