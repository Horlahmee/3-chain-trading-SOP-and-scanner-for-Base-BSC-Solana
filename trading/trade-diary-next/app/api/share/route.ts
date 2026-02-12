import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { text } = await req.json();
  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (!botToken || !chatId) {
    return NextResponse.json({ error: 'Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID' }, { status: 500 });
  }

  const res = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      disable_web_page_preview: true
    })
  });

  const data = await res.json();
  if (!res.ok || !data.ok) {
    return NextResponse.json({ error: 'Telegram send failed', details: data }, { status: 500 });
  }

  return NextResponse.json({ ok: true, messageId: data.result?.message_id });
}
