# Trading Toolkit (Super Genie)

## Files
- `SOP-3CHAIN.md` - execution and risk SOP for Base/BSC/Solana
- `scanner.py` - discovery + scoring scanner using DexScreener + CoinGecko
- `scan-output.json` - generated scan result

## Run
```bash
python trading/scanner.py
```

## Output
Scanner writes ranked candidates to:
- `trading/scan-output.json`

Each result includes:
- decision (`TRADE`, `WATCH`, `AVOID`)
- score
- liquidity / volume
- pair URL (DexScreener)
- explorer URL (BaseScan/BscScan/Solscan) for contract checks

## Notes
- Treat scanner as shortlist generation, not blind execution.
- Add GMGN feed later as an extra discovery source if needed.
