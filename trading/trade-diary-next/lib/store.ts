import fs from 'fs';
import path from 'path';

export type Trade = {
  id: number;
  createdAt: string;
  updatedAt: string;
  symbol: string;
  chain: 'base' | 'bsc' | 'solana';
  side: 'long' | 'short';
  entry?: number;
  exit?: number;
  sizeUsd?: number;
  pnlUsd?: number;
  status: 'open' | 'closed' | 'cancelled';
  conviction?: number;
  thesis?: string;
  invalidation?: string;
  result?: string;
  lesson?: string;
};

const dataDir = path.join(process.cwd(), 'data');
const filePath = path.join(dataDir, 'trades.json');

function ensure() {
  if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
  if (!fs.existsSync(filePath)) fs.writeFileSync(filePath, JSON.stringify({ trades: [] }, null, 2));
}

export function getTrades(): Trade[] {
  ensure();
  const raw = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return (raw.trades || []) as Trade[];
}

export function saveTrades(trades: Trade[]) {
  ensure();
  fs.writeFileSync(filePath, JSON.stringify({ trades }, null, 2));
}

export function addTrade(input: Partial<Trade>) {
  const trades = getTrades();
  const id = (trades[0]?.id || 0) + 1;
  const now = new Date().toISOString();
  const t: Trade = {
    id,
    createdAt: now,
    updatedAt: now,
    symbol: (input.symbol || '').toUpperCase(),
    chain: (input.chain as Trade['chain']) || 'base',
    side: (input.side as Trade['side']) || 'long',
    status: 'open',
    entry: input.entry,
    sizeUsd: input.sizeUsd,
    conviction: input.conviction,
    thesis: input.thesis,
    invalidation: input.invalidation
  };
  trades.unshift(t);
  saveTrades(trades);
  return t;
}

export function updateTrade(id: number, input: Partial<Trade>) {
  const trades = getTrades();
  const idx = trades.findIndex((t) => t.id === id);
  if (idx === -1) return null;
  trades[idx] = { ...trades[idx], ...input, updatedAt: new Date().toISOString() };
  saveTrades(trades);
  return trades[idx];
}
