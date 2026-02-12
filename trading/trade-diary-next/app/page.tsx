'use client';

import { useEffect, useMemo, useState } from 'react';

type Trade = {
  id: number;
  symbol: string;
  chain: string;
  side: string;
  status: string;
  entry?: number;
  exit?: number;
  sizeUsd?: number;
  pnlUsd?: number;
  conviction?: number;
  thesis?: string;
  invalidation?: string;
  result?: string;
  lesson?: string;
};

export default function Page() {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [form, setForm] = useState<any>({ chain: 'base', side: 'long' });
  const [post, setPost] = useState<any>({ status: 'closed' });
  const [pin, setPin] = useState('');
  const [unlocked, setUnlocked] = useState(false);

  const requiredPin = process.env.NEXT_PUBLIC_TRADE_DIARY_PIN || '1234';

  const load = async () => {
    const r = await fetch('/api/trades');
    const j = await r.json();
    setTrades(j.trades || []);
  };

  useEffect(() => {
    if (unlocked) load();
  }, [unlocked]);

  const create = async () => {
    await fetch('/api/trades', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    await load();
  };

  const closeTrade = async () => {
    await fetch(`/api/trades/${post.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(post)
    });
    await load();
  };

  const shareToTelegram = async (text: string) => {
    const r = await fetch('/api/share', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const j = await r.json();
    if (!r.ok) {
      alert(`Share failed: ${j.error || 'Unknown error'}`);
      return;
    }
    alert('Shared to Telegram ✅');
  };

  const preSummary = useMemo(
    () => `📘 PRE-TRADE\n${(form.symbol || '').toUpperCase()}/${form.chain} ${form.side}\nEntry: ${form.entry ?? '-'} | Size: $${form.sizeUsd ?? '-'}\nConviction: ${form.conviction ?? '-'}\nThesis: ${form.thesis ?? '-'}\nInvalidation: ${form.invalidation ?? '-'}`,
    [form]
  );

  const postSummary = useMemo(
    () => `📕 POST-TRADE\nTrade #${post.id ?? '-'}\nStatus: ${post.status}\nExit: ${post.exit ?? '-'} | PnL: $${post.pnlUsd ?? '-'}\nResult: ${post.result ?? '-'}\nLesson: ${post.lesson ?? '-'}`,
    [post]
  );

  const closed = trades.filter((t) => t.status === 'closed');
  const pnl = closed.reduce((a, t) => a + (t.pnlUsd || 0), 0);

  if (!unlocked) {
    return (
      <div className="wrap">
        <h2>Super Genie Trade Diary</h2>
        <div className="card">
          <h3>Unlock</h3>
          <input className="input" placeholder="Enter PIN" value={pin} onChange={(e) => setPin(e.target.value)} />
          <button onClick={() => setUnlocked(pin === requiredPin)}>Unlock</button>
          <p style={{ opacity: 0.7, fontSize: 12 }}>Set NEXT_PUBLIC_TRADE_DIARY_PIN in env for your own PIN.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="wrap">
      <h2>Super Genie Trade Diary</h2>

      <div className="card">
        <h3>Pre-Trade</h3>
        <div className="row">
          <input className="input" placeholder="Symbol" value={form.symbol || ''} onChange={(e) => setForm({ ...form, symbol: e.target.value })} />
          <select value={form.chain} onChange={(e) => setForm({ ...form, chain: e.target.value })}><option>base</option><option>bsc</option><option>solana</option></select>
        </div>
        <div className="row">
          <select value={form.side} onChange={(e) => setForm({ ...form, side: e.target.value })}><option>long</option><option>short</option></select>
          <input className="input" type="number" placeholder="Conviction" value={form.conviction || ''} onChange={(e) => setForm({ ...form, conviction: Number(e.target.value) })} />
        </div>
        <div className="row">
          <input className="input" type="number" placeholder="Entry" value={form.entry || ''} onChange={(e) => setForm({ ...form, entry: Number(e.target.value) })} />
          <input className="input" type="number" placeholder="Size USD" value={form.sizeUsd || ''} onChange={(e) => setForm({ ...form, sizeUsd: Number(e.target.value) })} />
        </div>
        <textarea placeholder="Thesis" value={form.thesis || ''} onChange={(e) => setForm({ ...form, thesis: e.target.value })} />
        <textarea placeholder="Invalidation" value={form.invalidation || ''} onChange={(e) => setForm({ ...form, invalidation: e.target.value })} />
        <div className="row">
          <button onClick={create}>Create Pre-Trade</button>
          <button onClick={() => shareToTelegram(preSummary)}>Share Pre to Telegram</button>
        </div>
      </div>

      <div className="card">
        <h3>Post-Trade</h3>
        <div className="row">
          <input className="input" type="number" placeholder="Trade ID" value={post.id || ''} onChange={(e) => setPost({ ...post, id: Number(e.target.value) })} />
          <select value={post.status} onChange={(e) => setPost({ ...post, status: e.target.value })}><option>closed</option><option>open</option><option>cancelled</option></select>
        </div>
        <div className="row">
          <input className="input" type="number" placeholder="Exit" value={post.exit || ''} onChange={(e) => setPost({ ...post, exit: Number(e.target.value) })} />
          <input className="input" type="number" placeholder="PnL USD" value={post.pnlUsd || ''} onChange={(e) => setPost({ ...post, pnlUsd: Number(e.target.value) })} />
        </div>
        <input className="input" placeholder="Result" value={post.result || ''} onChange={(e) => setPost({ ...post, result: e.target.value })} />
        <textarea placeholder="Lesson" value={post.lesson || ''} onChange={(e) => setPost({ ...post, lesson: e.target.value })} />
        <div className="row">
          <button onClick={closeTrade}>Save Post-Trade</button>
          <button onClick={() => shareToTelegram(postSummary)}>Share Post to Telegram</button>
        </div>
      </div>

      <div className="card">
        <h3>Review</h3>
        <p>Closed trades: {closed.length} | Net PnL: ${pnl.toFixed(2)}</p>
      </div>

      <div className="card">
        <h3>Recent Trades</h3>
        <table>
          <thead><tr><th>ID</th><th>Pair</th><th>Side</th><th>Status</th><th>PnL</th><th>Conv.</th></tr></thead>
          <tbody>
            {trades.map((t) => (
              <tr key={t.id}><td>{t.id}</td><td>{t.symbol}/{t.chain}</td><td>{t.side}</td><td>{t.status}</td><td>{t.pnlUsd ?? ''}</td><td>{t.conviction ?? ''}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
