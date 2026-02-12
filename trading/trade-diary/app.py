#!/usr/bin/env python3
import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).with_name("trades.db")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    c = conn()
    cur = c.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            symbol TEXT NOT NULL,
            chain TEXT NOT NULL,
            side TEXT NOT NULL,
            entry REAL,
            exit REAL,
            size_usd REAL,
            pnl_usd REAL,
            status TEXT NOT NULL DEFAULT 'open',
            conviction INTEGER,
            thesis TEXT,
            invalidation TEXT,
            result TEXT,
            lesson TEXT,
            tags TEXT
        )
        """
    )
    c.commit()
    c.close()


def add_pre(args):
    c = conn()
    cur = c.cursor()
    ts = now_iso()
    cur.execute(
        """
        INSERT INTO trades (
            created_at, updated_at, symbol, chain, side, entry, size_usd,
            status, conviction, thesis, invalidation, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'open', ?, ?, ?, ?)
        """,
        (
            ts,
            ts,
            args.symbol.upper(),
            args.chain.lower(),
            args.side.lower(),
            args.entry,
            args.sizeUsd,
            args.conviction,
            args.thesis,
            args.invalidation,
            args.tags,
        ),
    )
    trade_id = cur.lastrowid
    c.commit()
    c.close()
    print(f"Created pre-trade entry #{trade_id}")


def add_post(args):
    c = conn()
    cur = c.cursor()
    ts = now_iso()
    cur.execute(
        """
        UPDATE trades
        SET updated_at = ?,
            status = ?,
            exit = COALESCE(?, exit),
            pnl_usd = COALESCE(?, pnl_usd),
            result = COALESCE(?, result),
            lesson = COALESCE(?, lesson)
        WHERE id = ?
        """,
        (ts, args.status, args.exit, args.pnlUsd, args.result, args.lesson, args.id),
    )
    if cur.rowcount == 0:
        print("No trade found with that id")
    else:
        print(f"Updated post-trade entry #{args.id}")
    c.commit()
    c.close()


def list_trades(args):
    c = conn()
    cur = c.cursor()
    cur.execute(
        """
        SELECT id, created_at, symbol, chain, side, entry, exit, size_usd, pnl_usd, status, conviction
        FROM trades
        ORDER BY id DESC
        LIMIT ?
        """,
        (args.limit,),
    )
    rows = cur.fetchall()
    c.close()

    if not rows:
        print("No trades logged yet.")
        return

    for r in rows:
        print(
            f"#{r[0]} | {r[1]} | {r[2]} {r[4]} {r[3]} | entry={r[5]} exit={r[6]} | size=${r[7]} pnl=${r[8]} | {r[9]} | conv={r[10]}"
        )


def review(args):
    c = conn()
    cur = c.cursor()
    cur.execute(
        """
        SELECT id, symbol, chain, side, status, pnl_usd, conviction, thesis, result, lesson
        FROM trades
        ORDER BY id DESC
        LIMIT ?
        """,
        (args.limit,),
    )
    rows = cur.fetchall()
    c.close()

    if not rows:
        print("No data for review yet.")
        return

    total = len(rows)
    closed = [r for r in rows if r[4] == "closed"]
    wins = [r for r in closed if (r[5] or 0) > 0]
    losses = [r for r in closed if (r[5] or 0) < 0]
    pnl = sum((r[5] or 0) for r in closed)

    print("=== Trade Review ===")
    print(f"Total logged: {total}")
    print(f"Closed: {len(closed)} | Wins: {len(wins)} | Losses: {len(losses)}")
    print(f"Net PnL (closed): ${pnl:.2f}")
    if closed:
        print(f"Win rate: {(len(wins)/len(closed))*100:.1f}%")

    print("\nRecent lessons:")
    for r in rows:
        if r[9]:
            print(f"- #{r[0]} {r[1]} ({r[2]}): {r[9]}")


def main():
    p = argparse.ArgumentParser(description="Trade Diary App")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    pre = sub.add_parser("pre")
    pre.add_argument("--symbol", required=True)
    pre.add_argument("--chain", required=True, choices=["base", "bsc", "solana"])
    pre.add_argument("--side", required=True, choices=["long", "short"])
    pre.add_argument("--entry", type=float, required=True)
    pre.add_argument("--sizeUsd", type=float, required=True)
    pre.add_argument("--conviction", type=int, default=50)
    pre.add_argument("--thesis", required=True)
    pre.add_argument("--invalidation", required=True)
    pre.add_argument("--tags", default="")

    post = sub.add_parser("post")
    post.add_argument("--id", type=int, required=True)
    post.add_argument("--status", choices=["open", "closed", "cancelled"], default="closed")
    post.add_argument("--exit", type=float)
    post.add_argument("--pnlUsd", type=float)
    post.add_argument("--result")
    post.add_argument("--lesson")

    ls = sub.add_parser("list")
    ls.add_argument("--limit", type=int, default=20)

    rv = sub.add_parser("review")
    rv.add_argument("--limit", type=int, default=100)

    args = p.parse_args()

    if args.cmd == "init":
        init_db()
        print(f"Initialized {DB_PATH}")
    elif args.cmd == "pre":
        init_db()
        add_pre(args)
    elif args.cmd == "post":
        init_db()
        add_post(args)
    elif args.cmd == "list":
        init_db()
        list_trades(args)
    elif args.cmd == "review":
        init_db()
        review(args)


if __name__ == "__main__":
    main()
