# ONE-WEEK DESK WORKFLOW / OCT 13–20

## Day 0 — Co-PMs freeze contract (Tue Oct 13)
1. Download actual prices on one machine; inspect and copy to a PRIVATE shared repo or data store. Compute SHA-256 checksum (`shasum -a 256 data/prices.csv`). Freeze a commit ID and tag `sprint01-data-v1`. No analyst changes `main` data.
2. Walk through `src/backtest.py` together. Explain adjusted ETF prices vs tradeable fill prices, look-ahead, costs and benchmark limitations.
3. Assign 3 TEMP mixed-skill groups, each with a lead, implementer and reviewer. Give all three `data/prices.csv` and baseline outputs.
4. Each group creates branch `team-a-signal`, `team-b-backtest`, `team-c-risk` and completes own `teams/team_*.md`.

## Three teams work in parallel
- **A Signal**: research 63/126/252-day lookbacks and sign threshold, propose robust parameter setting. Owns `results/team_a_signals.csv` with `date,ticker,signal,lookback` (signal -1/0/1; for MVP map -1 to 0).
- **B Backtest/validation**: audit baseline logic, calculate portfolio and benchmark curves, time-split dates, verify costs/turnover. Owns `results/team_b_metrics.csv` and validation memo. This team does NOT consume Team A changes until baseline is audited.
- **C Risk overlay**: independently research volatility scaling at instrument or portfolio level using a trailing 63-day window and a capped total exposure. Owns `results/team_c_weights.csv` with `date,ticker,weight`. Must not peek at same-day returns.

## Integration interfaces
Team A signal output: `date,ticker,signal,lookback`, signal dated at observed close; any consumption for trades must occur after that close.
Team C weights output: `date,ticker,weight`, target weights with effective trade timestamp documented. The current toy backtest does NOT automatically ingest these custom weight files: integration requires an explicit code change and tests.
Team B: tests reference v0.1 independently and locks acceptance criteria. Co-PMs, not the teams, approve strategy change integration. A and C propose alternate scenarios, not guaranteed improvements.

## Gates and deadlines
- Oct 13: kickoff + paper + baseline walkthrough + tasks + frozen data
- Oct 14: each analyst reproduces baseline and confirms dataset checksum
- Oct 15: teams share research hypothesis and first artifact
- Oct 16: internal code review; B flags backtest validity issues; Co-PMs decide scope
- Oct 17–18: implement extensions, chronological 2010–2020 train / 2021–2023 validation / 2024–2026-10-09 held-out test (subject to instrument availability)
- Oct 19: freeze slide decks and results, disclose limitations
- Oct 20: three **8-minute presentations + 4-minute Q&A**, Co-PM review, permanent team assignment

## Review rules
Never select parameters on the held-out test period. If a model is changed after viewing the test result, record the test as contaminated. Flag survivorship and vendor-adjustment issues, ETF inception dates, execution assumptions, covariance estimation choices, and benchmark cost mismatches. No capital deployment from Sprint 01.
