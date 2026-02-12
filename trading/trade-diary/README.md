# Trade Diary App (Shared Playbook)

A lightweight trade journaling system for **before + after** documentation on every trade.

## Why
This enforces process discipline and creates a reviewable learning loop:
- pre-trade thesis and conviction are captured before execution
- post-trade outcomes and lessons are captured after execution
- performance can be reviewed over time

## Files
- `app.py` — CLI app for journaling and review
- `trades.db` — SQLite database (auto-created)

## Quick Start
```bash
python trading/trade-diary/app.py init
python trading/trade-diary/app.py pre --symbol BRETT --chain base --side long --entry 0.123 --sizeUsd 150 --conviction 72 --thesis "Breakout + narrative momentum" --invalidation "Loses key level and volume collapses"
python trading/trade-diary/app.py post --id 1 --status closed --exit 0.158 --pnlUsd 42 --result "Win" --lesson "Scaled out too late; tighten TP ladder"
python trading/trade-diary/app.py list --limit 20
python trading/trade-diary/app.py review --limit 50
```

## Required Workflow (for every trade)
1. Create **pre-trade** entry before execution (`pre` command)
2. Execute trade
3. Add **post-trade** update (`post` command)
4. Review weekly (`review` command)

## Shared Access
Because this is in your repo/workspace, both of us can read and update it.
