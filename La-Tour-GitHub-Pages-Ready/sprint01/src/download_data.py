"""Download REAL split/dividend-adjusted ETF prices. Requires Internet access."""
import csv
from pathlib import Path
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
TICKERS = ['SPY', 'IEF', 'GLD', 'UUP']
START, END = '2010-01-01', '2026-10-10'  # End is exclusive; frozen through Oct 9, 2026.

def main():
    dest = ROOT / 'data' / 'prices.csv'
    all_rows=[]
    for ticker in TICKERS:
        df=yf.download(ticker,start=START,end=END,auto_adjust=True,progress=False,threads=False)
        if df.empty: raise RuntimeError(f'No data for {ticker}; do not use synthetic fixture for performance reporting')
        close=df['Close']
        if hasattr(close,'columns'): close=close.iloc[:,0]
        for date, price in close.dropna().items():
            all_rows.append([date.strftime('%Y-%m-%d'),ticker,round(float(price),8)])
    all_rows.sort(key=lambda x:(x[0],x[1]))
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('w',newline='') as fh:
        w=csv.writer(fh);w.writerow(['date','ticker','adj_close']);w.writerows(all_rows)
    print(f'Wrote {len(all_rows)} authentic observed ETF observations to {dest}. Latest date: {all_rows[-1][0]}')
    print('Check missing trading days, vendor adjustments, and price-source licensing before research use.')

if __name__=='__main__': main()
