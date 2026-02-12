# Mandatory Trade Logging Rules

From now on, every trade must be documented in two stages:

1. **Pre-Trade (before execution)**
   - symbol, chain, side, entry
   - position size (USD)
   - conviction score (0-100)
   - thesis
   - invalidation

2. **Post-Trade (after execution/close)**
   - exit
   - realized PnL
   - result (win/loss/breakeven)
   - lesson learned

## Commands
```bash
python trading/trade-diary/app.py pre ...
python trading/trade-diary/app.py post ...
python trading/trade-diary/app.py list --limit 20
python trading/trade-diary/app.py review --limit 100
```

## Objective
Build a compounding learning loop so future trade quality improves through structured review.
