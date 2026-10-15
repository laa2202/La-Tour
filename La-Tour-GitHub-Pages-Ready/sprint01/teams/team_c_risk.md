# TEAM C — RISK & OVERLAYS
**Hypothesis:** A volatility overlay may improve exposure stability, not necessarily alpha.
**Beginner:** Estimate rolling 63-day annualized volatility; compare across SPY, IEF, GLD, UUP.
**Experienced:** Implement inverse-volatility or capped risk targeting using only information from previous close; document target-volatility parameter and leverage caps.
**Output:** `results/team_c_weights.csv` with `date,ticker,weight`; memo on leverage, turnover, and risk attribution.
**Presentation:** What risks remain? How much risk each ETF contributes? How does the overlay affect drawdown and transaction costs?
