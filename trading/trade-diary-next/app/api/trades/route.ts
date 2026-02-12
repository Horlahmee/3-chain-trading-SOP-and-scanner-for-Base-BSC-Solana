import { NextRequest, NextResponse } from 'next/server';
import { addTrade, getTrades } from '@/lib/store';

export async function GET() {
  return NextResponse.json({ trades: getTrades() });
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const trade = addTrade({
    symbol: body.symbol,
    chain: body.chain,
    side: body.side,
    entry: body.entry,
    sizeUsd: body.sizeUsd,
    conviction: body.conviction,
    thesis: body.thesis,
    invalidation: body.invalidation
  });
  return NextResponse.json({ trade });
}
