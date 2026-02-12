import { NextRequest, NextResponse } from 'next/server';
import { updateTrade } from '@/lib/store';

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  const body = await req.json();
  const trade = updateTrade(Number(params.id), {
    status: body.status,
    exit: body.exit,
    pnlUsd: body.pnlUsd,
    result: body.result,
    lesson: body.lesson
  });
  if (!trade) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json({ trade });
}
