#!/usr/bin/env python3
import json
import math
import time
import urllib.parse
import urllib.request
from typing import Dict, List, Any

DEX_BASE = "https://api.dexscreener.com"
CG_BASE = "https://api.coingecko.com/api/v3"

CHAIN_CONFIG = {
    "base": {"min_liq": 35_000, "min_vol24": 80_000, "queries": ["base", "brett", "toshi", "degen", "meme"]},
    "bsc": {"min_liq": 50_000, "min_vol24": 120_000, "queries": ["bsc", "bnb", "meme", "ai", "doge"]},
    "solana": {"min_liq": 40_000, "min_vol24": 100_000, "queries": ["sol", "solana", "bonk", "wif", "meme"]},
}

EXPLORER = {
    "base": "https://basescan.org/token/{token}",
    "bsc": "https://bscscan.com/token/{token}",
    "solana": "https://solscan.io/token/{token}",
}


def fetch_json(url: str, timeout: int = 20) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": "SuperGenie-Scanner/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_pairs(query: str) -> List[Dict[str, Any]]:
    q = urllib.parse.quote(query)
    url = f"{DEX_BASE}/latest/dex/search?q={q}"
    data = fetch_json(url)
    return data.get("pairs", []) if isinstance(data, dict) else []


def get_market_context() -> Dict[str, Any]:
    url = f"{CG_BASE}/global"
    data = fetch_json(url)
    d = data.get("data", {}) if isinstance(data, dict) else {}
    return {
        "total_mcap_usd": d.get("total_market_cap", {}).get("usd"),
        "total_vol_usd": d.get("total_volume", {}).get("usd"),
        "btc_dominance": d.get("market_cap_percentage", {}).get("btc"),
        "active_cryptos": d.get("active_cryptocurrencies"),
        "updated_at": int(time.time()),
    }


def score_pair(p: Dict[str, Any]) -> float:
    liq = float((p.get("liquidity") or {}).get("usd") or 0)
    vol24 = float((p.get("volume") or {}).get("h24") or 0)
    tx_h1 = (p.get("txns") or {}).get("h1") or {}
    buys = float(tx_h1.get("buys") or 0)
    sells = float(tx_h1.get("sells") or 0)
    flow = (buys + 1.0) / (sells + 1.0)

    chg1 = float((p.get("priceChange") or {}).get("h1") or 0)
    chg24 = float((p.get("priceChange") or {}).get("h24") or 0)

    liq_score = min(30.0, math.log10(max(liq, 1)) * 6)
    vol_score = min(30.0, math.log10(max(vol24, 1)) * 6)
    flow_score = max(0.0, min(20.0, flow * 6))
    momentum_score = max(0.0, min(20.0, (chg1 * 1.2 + chg24 * 0.3) / 2.5 + 10))

    return round(liq_score + vol_score + flow_score + momentum_score, 2)


def classify(score: float, liq: float, vol24: float, cfg: Dict[str, Any]) -> str:
    if liq < cfg["min_liq"] or vol24 < cfg["min_vol24"]:
        return "AVOID"
    if score >= 70:
        return "TRADE"
    if score >= 55:
        return "WATCH"
    return "AVOID"


def chain_filter(chain: str, pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [p for p in pairs if (p.get("chainId") or "").lower() == chain]


def dedupe_pairs(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for p in pairs:
        key = (p.get("chainId"), p.get("pairAddress"))
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def build_report() -> Dict[str, Any]:
    report = {
        "generated_at": int(time.time()),
        "market_context": get_market_context(),
        "results": {},
        "notes": [
            "GMGN discovery can be added as extra input feed.",
            "Explorer links are provided for manual contract checks before execution.",
            "This is a research scanner, not autonomous execution advice.",
        ],
    }

    for chain, cfg in CHAIN_CONFIG.items():
        raw = []
        for q in cfg["queries"]:
            raw.extend(chain_filter(chain, search_pairs(q)))

        pairs = dedupe_pairs(raw)
        ranked = []
        for p in pairs:
            liq = float((p.get("liquidity") or {}).get("usd") or 0)
            vol24 = float((p.get("volume") or {}).get("h24") or 0)
            s = score_pair(p)
            token = (p.get("baseToken") or {}).get("address") or ""
            ranked.append({
                "decision": classify(s, liq, vol24, cfg),
                "score": s,
                "chain": chain,
                "dex": p.get("dexId"),
                "pair_address": p.get("pairAddress"),
                "pair_url": p.get("url"),
                "token_symbol": (p.get("baseToken") or {}).get("symbol"),
                "token_name": (p.get("baseToken") or {}).get("name"),
                "token_address": token,
                "explorer": EXPLORER[chain].format(token=token) if token else None,
                "price_usd": p.get("priceUsd"),
                "liq_usd": liq,
                "vol24_usd": vol24,
                "txns_h1": (p.get("txns") or {}).get("h1"),
                "price_change": p.get("priceChange"),
                "fdv": p.get("fdv"),
                "market_cap": p.get("marketCap"),
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)
        report["results"][chain] = ranked[:30]

    return report


def main():
    report = build_report()
    out = "trading/scan-output.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Wrote {out}")
    for chain, items in report["results"].items():
        top = items[:5]
        print(f"\n[{chain.upper()}] top {len(top)}")
        for i, row in enumerate(top, 1):
            print(
                f"{i}. {row['token_symbol']} | {row['decision']} | score={row['score']} | liq=${row['liq_usd']:.0f} | vol24=${row['vol24_usd']:.0f}"
            )


if __name__ == "__main__":
    main()
