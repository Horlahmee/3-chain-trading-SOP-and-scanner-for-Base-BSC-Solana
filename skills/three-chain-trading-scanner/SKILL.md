---
name: three-chain-trading-scanner
description: Scan and rank meme/token candidates across Base, BSC, and Solana using DexScreener discovery plus CoinGecko market context, then classify candidates as TRADE/WATCH/AVOID with explorer links for contract checks. Use when the user asks for multi-chain token discovery, degen watchlists, quick market scans, shortlist generation, or repeatable pre-trade filtering.
---

# Three-Chain Trading Scanner

Run a repeatable research scan for Base, BSC, and Solana, then return a concise shortlist with risk-aware classifications.

## Workflow

1. Run the scanner script:
   - `python skills/three-chain-trading-scanner/scripts/scanner.py`
2. Read output JSON:
   - `trading/scan-output.json`
3. Report the top candidates per chain with:
   - decision (`TRADE`, `WATCH`, `AVOID`)
   - score
   - liquidity / 24h volume
   - pair URL (DexScreener)
   - explorer URL (BaseScan/BscScan/Solscan)
4. Require manual contract checks before execution.

## Required Risk Behavior

- Treat output as a research shortlist, not blind execution.
- Reject candidates below liquidity/volume floors.
- Favor entries after pullback/consolidation, not vertical tops.
- Use staged profit-taking and predefined invalidation.

For the full policy and thresholds, read:
- `references/sop-3chain.md`

## Script

- `scripts/scanner.py`
  - Pulls DexScreener search candidates
  - Pulls CoinGecko global context
  - Scores momentum + flow + liquidity + volume
  - Writes ranked output JSON for Base/BSC/Solana

## Output Contract

Primary output file:
- `trading/scan-output.json`

Expected consumer behavior:
- summarize top 3-5 per chain
- highlight only high-conviction setups
- include explicit risks and invalidation criteria
