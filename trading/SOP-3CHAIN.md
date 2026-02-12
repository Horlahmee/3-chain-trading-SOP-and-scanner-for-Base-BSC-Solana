# Super Genie 3-Chain Degen SOP (Base + BSC + Solana)

## 0) Mission
Find asymmetric meme/token opportunities while minimizing obvious rugs and bad liquidity traps.

## 1) Data Stack
- **Pricing / market context:** CoinGecko
- **Discovery:** DexScreener, GMGN
- **Contract + token checks:**
  - Base: BaseScan
  - BSC: BscScan
  - Solana: Solscan

## 2) Hard Risk Rules (Non-Negotiable)
1. Max risk per trade: **1.5% bankroll** (2.5% only for A+ setups)
2. Max open meme positions: **5**
3. Daily stop: **-6% bankroll** → stop new entries for 24h
4. Never enter if estimated slippage is too high for position size
5. Never average down blindly after major thesis break

## 3) Discovery Flow
1. Pull candidates from DexScreener (search/trending patterns)
2. Add fresh GMGN candidates (manual or integration)
3. Keep only chains: `base`, `bsc`, `solana`
4. Remove obvious dead pools / zero-liquidity pairs

## 4) Minimum Filters (per candidate)
- Liquidity floor:
  - Base: **>= $35k**
  - BSC: **>= $50k**
  - Solana: **>= $40k**
- 24h volume floor:
  - Base: **>= $80k**
  - BSC: **>= $120k**
  - Solana: **>= $100k**
- Recent activity: meaningful txns in h1/h24 (not only 1 wallet looping)
- Pair age: not too old/dead and not only a few minutes old without confirmation

## 5) Contract / Token Verification Checklist
Before entry, check explorer links:

### Base (BaseScan)
- Contract verified?
- Suspicious owner privileges?
- Transfer tax / blacklist / pause / mint surprises?
- Holder distribution concentration red flags?

### BSC (BscScan)
- Same checks as Base
- Extra caution for copycat contracts and stealth taxes

### Solana (Solscan)
- Token metadata sanity
- Top holder concentration
- Mint/freeze authority behavior (if applicable)
- LP and pool legitimacy on actual venue

## 6) Entry Rules
- Avoid buying straight vertical candles
- Preferred entries:
  - First clean pullback after breakout
  - Sideways consolidation with stable volume
- If narrative strength is weak or purely paid shill, reduce size or skip

## 7) Exit Rules
- Take profit ladder:
  - 25% at 2x
  - 25% at 3-5x zone
  - 25% at 8-10x zone
  - Keep 25% moon bag only if trend + volume remain strong
- Hard exit triggers:
  - Volume collapse + liquidity drain
  - Whale dump / obvious insider unloading
  - News or contract red flag invalidates thesis

## 8) Trade Classification
- **TRADE**: passes filters + clean structure + narrative + risk acceptable
- **WATCH**: promising but incomplete confirmation
- **AVOID**: fails risk checks, bad contract signals, or poor liquidity quality

## 9) Execution Notes
- Use scanner output as shortlist, not blind auto-buy
- Validate contract details before position opens
- Log every trade reason + invalidation + outcome for iteration

---

## Fast Daily Loop (15-30 min)
1. Run scanner
2. Review top 10 by score
3. Open explorer links for top 3-5
4. Produce TRADE/WATCH/AVOID table
5. Execute only if risk limits allow
