# LA TOUR — Quant Research Sprint 01
**Crown & Dagger | Fall 2026**

**Deadline:** Sunday, October 25, 2026  
**Co-PMs:** Leen and Jana  
**Research strategy:** Time-Series Momentum  
**Deliverables:** Code, CSV results, research memo, and six-slide presentation

---

## Sprint 01 — Analyst Assignment & Instructions

### Your Objective

This week, you will investigate whether a systematic trend-following strategy can produce useful investment signals across four financial markets.

You will learn to retrieve market data, calculate trading signals, simulate historical performance, identify weaknesses in quantitative models, and defend a research recommendation.

Your goal is not to produce the highest possible return. Your goal is to produce credible, reproducible research.

By the end of this exercise, you should understand how a quantitative research idea moves from an economic hypothesis to an algorithm, then to a backtest, and finally to an investment research decision.

### Team Assignments

| Team | Members | Focus |
|---|---|---|
| Team A | Cooper, Kaka, Ken | Signal Research |
| Team B | Kai, Jonas | Backtesting & Validation |
| Team C | Leen, Jana | Portfolio Risk |

All teams begin with the same baseline strategy and historical dataset. Each group investigates a separate component of the research process.

---

## Step 1 — Understand the Strategy

### What are we researching?

Our starting point is a simplified version of *Time Series Momentum*, a strategy studied by Moskowitz, Ooi, and Pedersen (2012).

The underlying idea is that assets with positive historical price trends may continue exhibiting positive trends over subsequent periods.

We want to test whether that idea produces useful trading signals and how sensitive the results are to our assumptions.

### The assets

We will use four exchange-traded funds (ETFs):

- **SPY:** U.S. equities
- **IEF:** U.S. Treasury bonds
- **GLD:** Gold
- **UUP:** U.S. dollar exposure

These ETFs serve as simplified proxies for different macroeconomic markets.

### How the baseline algorithm works

Our baseline algorithm examines each ETF's trailing 252-trading-day return using information available by the previous close.

A positive return gives that ETF a 25% target portfolio weight. A zero or negative return gives it a 0% weight. Remaining capital stays in cash.

For example, if SPY and GLD have positive signals while IEF and UUP have negative signals, the target portfolio is:

| Asset | Portfolio Weight |
|---|---|
| SPY | 25% |
| IEF | 0% |
| GLD | 25% |
| UUP | 0% |
| Cash | 50% |

The portfolio is rebalanced monthly.

The baseline charges 5 basis points per unit of absolute weight turnover. Cash earns 0% in this simplified model.

This is a research simulation with known execution limitations, not an executable trading system.

### What is a trading signal?

A signal is a numerical instruction derived from data.

For example:

- Positive trailing return: positive trend signal
- Negative trailing return: negative trend signal
- No positive signal: no allocation to that asset

The signal determines the portfolio's target allocation according to the baseline rules.

Your task is to investigate whether the signal construction, historical performance, or portfolio allocation could be improved or better understood.

---

## Step 2 — Set Up Your Environment

Every analyst must complete the environment setup before starting individual team research.

### 2.1 Clone the repository

Open Terminal and run:

```bash
git clone https://github.com/laa2202/La-Tour.git
cd La-Tour/sprint01
```

This downloads the repository to your computer and navigates to the Sprint 01 research directory.

### 2.2 Create a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows, use the appropriate activation command for your terminal.

A virtual environment keeps this project's Python dependencies separate from other projects.

### 2.3 Install dependencies

```bash
pip install -r requirements.txt
```

This installs the packages needed to execute the research scripts, including the market-data downloader dependency.

### 2.4 Download historical market data

```bash
python src/download_data.py
```

The downloader requests historical adjusted daily prices for SPY, IEF, GLD, and UUP.

The intended historical period is January 1, 2010, through October 9, 2026, subject to actual data availability.

Verify that `data/prices.csv` contains these columns:

```text
date,ticker,adj_close
```

Where:

- `date` identifies the trading date.
- `ticker` identifies the ETF.
- `adj_close` represents its adjusted closing price.

Verify that dates are correctly formatted and that each ETF's available observations have been recorded.

### 2.5 Verify the dataset

Run:

```bash
shasum -a 256 data/prices.csv
```

Record the resulting checksum, data source, download timestamp, and date coverage.

All teams must use the same frozen dataset.

If the downloader fails, contact the Co-PMs for the approved dataset. Synthetic data is for debugging only.

### 2.6 Run the baseline backtest

```bash
python src/backtest.py --input data/prices.csv --output results/base.csv
```

This runs the baseline strategy using the historical price dataset.

The output contains the strategy's historical simulation results.

### 2.7 Run the unit tests

```bash
python -m unittest discover -s tests -v
```

Confirm that the reference tests pass before changing the research code.

### 2.8 If the market-data download fails

Use the provided synthetic dataset generator to confirm that the implementation can execute:

```bash
python src/generate_synthetic_fixture.py

python src/backtest.py --input data/SYNTHETIC_TEST_ONLY_prices.csv --output results/TEST_ONLY.csv
```

Synthetic data must not be used as evidence of actual market performance.

---

## Step 3 — Reproduce the Baseline

Before modifying the model, every analyst must understand:

1. How the historical price data is collected.
2. How a trailing return is calculated.
3. How that return becomes a trading signal.
4. How signals determine portfolio allocations.
5. How portfolio returns and transaction costs are calculated.
6. Why historical simulation results may differ from achievable real-world performance.

### Your task

Open `src/backtest.py` and follow the calculations from the historical prices to the final strategy returns.

Identify where the program:

- Reads the dataset.
- Calculates returns.
- Generates momentum signals.
- Determines portfolio weights.
- Applies rebalancing rules.
- Calculates portfolio performance.
- Accounts for transaction costs.

Run the reference backtest and explain at least one historical trading decision.

For that decision, identify the historical prices used, the resulting momentum signal, the target portfolio allocation, and the subsequent return calculation.

**Every analyst must be able to explain the baseline before beginning team-specific extensions.**

---

## Step 4 — Complete Your Assigned Research

### Team A — Signal Research

**Members:** Cooper, Kaka, Ken

**Research question:** How does the length of a momentum signal's lookback window affect its behavior?

#### Background

The baseline uses 252 trading days of historical returns to decide whether an asset has a positive trend.

However, this observation window is a modeling assumption.

A shorter window may react more quickly to recent price changes but may also generate more frequent signal changes.

A longer window may produce more stable signals but respond more slowly to market reversals.

Your task is to investigate that trade-off.

#### Instructions

1. Reproduce the original 252-day momentum signal.
2. Calculate alternative 63-day and 126-day signals.
3. Compare all three lookback windows across ETFs and historical periods.
4. Measure signal stability and switching frequency.
5. Evaluate whether changes improve robustness without using held-out test data for parameter selection.
6. Explain which signal, if any, merits further testing.

#### Questions to investigate

- How frequently does each signal switch between positive and negative?
- Do shorter lookback windows detect trend reversals faster?
- Are longer lookback windows more stable?
- Do the results differ between equities, bonds, gold, and dollar exposure?
- Are apparent improvements consistent across different historical periods?
- Does any preferred lookback remain convincing after transaction costs and validation?

#### Required CSV

`results/team_a_signals.csv`

Columns:

```text
date,ticker,signal,lookback
```

Document how signal values are defined. The baseline remains long-or-cash: negative signals do not automatically become short positions.

#### Final recommendation

Explain which lookback specification deserves further research and what evidence supports your recommendation.

---

### Team B — Backtesting & Validation

**Members:** Kai, Jonas

**Research question:** Can we trust the strategy's backtested performance?

#### Background

A backtest simulates how a strategy would have performed using historical observations.

However, backtests can give misleading results when they use future information, unrealistic trading assumptions, incorrect return calculations, or incomplete transaction costs.

Your job is to evaluate whether the baseline simulation provides reliable evidence.

#### Instructions

1. Reproduce the baseline backtest independently.
2. Check for look-ahead bias and incorrect return timing.
3. Calculate CAGR, volatility, Sharpe ratio, maximum drawdown, and turnover.
4. Compare the strategy against the supplied benchmark.
5. Examine transaction costs and unrealistic execution assumptions.
6. Explain which results are credible and which assumptions require correction.

#### Metrics to calculate

**CAGR — Compound Annual Growth Rate**

The annualized growth rate implied by the portfolio's cumulative performance.

**Volatility**

A measure of the variability of strategy returns.

**Sharpe Ratio**

A measure of excess return relative to return volatility. State the risk-free-rate convention used.

**Maximum Drawdown**

The largest percentage decline in cumulative portfolio value from a previous peak.

**Turnover**

A measure of how much the strategy changes its portfolio positions over time.

#### Questions to investigate

- Are the signals based entirely on information available at the time?
- Is the simulated portfolio return calculated using the correct holding period?
- Are transaction costs applied correctly?
- How frequently does the strategy rebalance?
- Are the benchmark assumptions comparable to the strategy assumptions?
- Would different execution assumptions change the interpretation of the results?

The reference implementation includes a simplified previous-close execution assumption that is not directly executable. Identify and explain this limitation.

#### Required CSV

`results/team_b_metrics.csv`

Columns:

```text
sample,strategy,cagr,volatility,sharpe,max_drawdown,turnover
```

#### Final recommendation

State whether the existing backtest is suitable for further research and which components should be corrected before more advanced strategy development.

---

### Team C — Portfolio Risk

**Members:** Leen, Jana

**Research question:** Can volatility-based position sizing improve portfolio risk management?

#### Background

The baseline strategy assigns an equal 25% target weight to every ETF exhibiting a positive signal.

However, equal capital allocation does not necessarily imply equal risk allocation.

Different assets experience different levels of volatility.

A more volatile ETF may contribute disproportionately to portfolio risk despite receiving the same capital weight as a less volatile ETF.

Your task is to investigate whether alternative position-sizing rules can produce a more controlled risk profile.

#### Instructions

1. Reproduce baseline allocations.
2. Calculate trailing 63-day volatility for each ETF.
3. Investigate inverse-volatility weights or a capped risk-targeting approach.
4. Explain how weights are normalized, capped, and adjusted when signals turn off.
5. Evaluate exposure, concentration, turnover, estimated costs, and drawdowns.
6. Explain whether the alternative allocation is sufficiently robust for further research.

#### Questions to investigate

- Which assets exhibit the greatest historical volatility?
- Does the baseline portfolio concentrate risk in particular assets?
- How would inverse-volatility weighting change the portfolio's allocations?
- Do alternative weights introduce additional turnover?
- What happens when volatility increases significantly?
- Does the proposed approach reduce drawdown or merely shift the portfolio's exposures?
- How sensitive are the results to the volatility estimation window?

#### Required CSV

`results/team_c_weights.csv`

Columns:

```text
date,ticker,weight
```

Custom weights require explicit backtest integration and testing before performance claims can be made.

#### Final recommendation

Explain whether a volatility-aware allocation approach is worth further investigation and identify the main implementation challenges.

---

## Step 5 — Validate Your Findings

All teams must evaluate their research using chronological data splits.

| Period | Dates | Purpose |
|---|---|---|
| Training | 2010–2020 | Develop hypotheses |
| Validation | 2021–2023 | Compare proposed approaches |
| Held-out test | 2024–October 9, 2026 | Evaluate final choices |

Use only available observations and account for ETF inception dates.

### Training period

Use the training period to understand the strategy, investigate hypotheses, and develop candidate approaches.

### Validation period

Use the validation period to compare candidate approaches and examine whether the findings remain consistent outside the original training sample.

### Held-out test period

Use the final held-out period to evaluate the selected methodology without further parameter optimization.

Do not optimize a strategy on held-out test results.

If you modify a strategy after examining its held-out performance, disclose that the test period has influenced model selection.

### Required validation standards

All teams must:

1. Verify that historical calculations do not use unavailable future information.
2. Clearly distinguish the original baseline from proposed modifications.
3. Document their dataset and assumptions.
4. Report relevant transaction costs.
5. Discuss benchmark limitations.
6. Identify weaknesses and failure cases.
7. Explain whether their findings are robust across historical periods.

A model that looks attractive in one specific period but fails in other periods should not automatically be considered an improvement.

---

## Step 6 — Prepare Your Final Deliverables

Each team must submit by **Sunday, October 25, 2026**:

### 1. Reproducible Python code

Submit the scripts used to conduct your experiment.

Include the commands necessary to reproduce the analysis.

### 2. Team-specific CSV results

Submit the required CSV file for your assigned team.

Ensure all columns use the specified names and that the results can be regenerated from your code.

### 3. Research memo

Your memo must explain:

- The research question.
- The economic or mathematical intuition.
- The dataset and assumptions.
- The methodology and implementation.
- The results.
- The robustness checks.
- The limitations.
- The final recommendation.

### 4. Visualizations

Include performance or diagnostic figures relevant to your experiment.

Figures should have clearly labeled axes, units, and historical periods.

### 5. Six-slide presentation

Each team must prepare a six-slide research defense summarizing its work.

### 6. Final recommendation

Select one of the following:

- **Reject:** The evidence does not justify continued work on the proposed approach.
- **Continue research:** The idea has sufficient support to justify additional investigation.
- **Requires further validation:** The current evidence is insufficient to reach a defensible conclusion.

Support your recommendation with the findings of your experiment.

---

## Step 7 — Research Defense

Each team has **8 minutes to present and 4 minutes for Q&A**.

### Required slide structure

**Slide 1 — Hypothesis**

What are we testing, and why might it work?

**Slide 2 — Data**

What data did we collect, and what are its limitations?

**Slide 3 — Methodology**

How does the proposed algorithm work?

What calculations did we implement?

**Slide 4 — Results**

What happened in the historical experiment?

Include quantitative evidence and comparisons.

**Slide 5 — Robustness**

What could invalidate the findings?

Discuss methodological weaknesses, assumptions, sensitivity, and failure cases.

**Slide 6 — Recommendation**

Should we reject, continue, or conduct additional validation?

Explain the decision using the evidence presented.

### Presentation expectations

Every member should understand the team's overall research question and methodology.

Be prepared to explain your calculations, defend your assumptions, and discuss your model's weaknesses.

The goal is to demonstrate sound research judgment, not merely show attractive performance charts.

---

## Research Standards

We value methodological rigor over attractive performance numbers.

Your results must be reproducible, transparent, and supported by evidence.

Disclose weaknesses, unrealistic assumptions, sensitivity to parameters, and potential sources of bias.

A negative result supported by rigorous analysis is a successful research outcome.

**No strategies are authorized for live capital deployment during Sprint 01.**
