# La Tour / Crown & Dagger Quant Pod Site

Static GitHub Pages site with the official user-provided lion asset.

- `index.html`: research desk homepage with Sprint 01 link.
- `lectures/01.html`: original seven-slide briefing.
- `lectures/02-sprint-walkthrough.html`: detailed interactive 26-slide implementation walkthrough, code, tests and speaker notes. Navigate with arrows; N toggles presenter notes; select jumps between slides. Copy buttons work when hosted over HTTPS.
- `sprint01/`: source code, downloader, reproducibility tests, **synthetic** test fixture, three team tasks, and research templates.

## Publish
Upload ZIP contents (not ZIP itself) to public GitHub Pages repository. The starter exercises are public but fund-private data, API secrets, portfolio details or proprietary algorithms MUST be in separate private repository. Download real adjusted ETF data using commands in `sprint01/README.md` after cloning locally.

Run `python -m unittest discover -s tests -v` from `sprint01/` to verify reference tests. Real dataset is not included. Synthetic data is strictly for execution tests.


## Fall 26 Recruiting Pitches
Five PDF pitch decks are located at `recruiting/fall-2026/` and linked from the homepage. Verify permission to publish externally before enabling this section on a public GitHub Pages site.

## NEW — Quant Research A–Z onboarding
The Sprint 01 deck now begins with 23 beginner-first slides covering fund/QR terminology, strategy choice, data, signals, coding in Python and C, returns, backtest timing, research mistakes, three-team workflows, and a readiness quiz. The original 26-slide implementation deep dive follows.

## Interactive pitch-to-trade case

Open `lectures/03-pitch-to-trade.html` (Joni Chilean peso/copper recruiting pitch). This is a teaching case based on an unverified candidate pitch, with illustrative assumptions, interactive sliders, gated decision exercises, and team workflow. No live-trade approval is implied.
