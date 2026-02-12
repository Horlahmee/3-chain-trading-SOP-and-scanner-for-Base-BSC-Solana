# Trade Diary Next.js App

Mobile-friendly web app for pre-trade and post-trade logging.

## Run
```bash
cd trading/trade-diary-next
npm install
```

Create `.env.local`:
```bash
NEXT_PUBLIC_TRADE_DIARY_PIN=1234
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=7179104033
```

Then run:
```bash
npm run dev
```

Open:
- Local: `http://localhost:3001`
- Phone (same Wi-Fi): `http://<YOUR_PC_LAN_IP>:3001`

## Features
- Pre-trade logging (symbol/chain/entry/size/conviction/thesis/invalidation)
- Post-trade update (status/exit/pnl/result/lesson)
- Review summary (closed count + net PnL)
- Recent trade table

## Data
Stored in:
- `trading/trade-diary-next/data/trades.json`
