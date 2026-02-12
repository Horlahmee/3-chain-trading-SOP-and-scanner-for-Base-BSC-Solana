# Phone Access Setup (Trade Diary)

## 1) Start app
```bash
python trading/trade-diary/mobile_web_app.py
```

## 2) Open on your phone (same Wi-Fi)
Find your PC LAN IP (example `192.168.1.20`) and open:

`http://<PC_LAN_IP>:8787`

## 3) Optional internet access
Use a tunnel (Cloudflare/ngrok/Tailscale funnel) and share the public URL.

---

This app writes to the same `trading/trade-diary/trades.db` journal used by the CLI.
