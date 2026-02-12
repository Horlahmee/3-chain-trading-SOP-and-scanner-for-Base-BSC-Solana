#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "trades.db"
HOST = "0.0.0.0"
PORT = 8787

HTML = r'''<!doctype html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Trade Diary</title>
<style>body{font-family:Arial;margin:12px;background:#0b1020;color:#e8ecff}.card{background:#131a33;padding:12px;border-radius:12px;margin-bottom:12px}input,select,textarea,button{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:1px solid #334}button{background:#4f7cff;color:#fff;border:0}table{width:100%;font-size:12px}td,th{padding:6px;border-bottom:1px solid #223}.row{display:grid;grid-template-columns:1fr 1fr;gap:8px}</style>
</head><body>
<h2>Super Genie Trade Diary</h2>
<div class="card"><h3>Pre-Trade</h3>
<div class='row'><input id='symbol' placeholder='Symbol'><select id='chain'><option>base</option><option>bsc</option><option>solana</option></select></div>
<div class='row'><select id='side'><option>long</option><option>short</option></select><input id='conv' type='number' placeholder='Conviction 0-100'></div>
<div class='row'><input id='entry' type='number' step='any' placeholder='Entry'><input id='size' type='number' step='any' placeholder='Size USD'></div>
<textarea id='thesis' placeholder='Thesis'></textarea>
<textarea id='inv' placeholder='Invalidation'></textarea>
<button onclick='createTrade()'>Create Pre-Trade</button></div>

<div class="card"><h3>Post-Trade</h3>
<div class='row'><input id='tid' type='number' placeholder='Trade ID'><select id='status'><option>closed</option><option>open</option><option>cancelled</option></select></div>
<div class='row'><input id='exit' type='number' step='any' placeholder='Exit'><input id='pnl' type='number' step='any' placeholder='PnL USD'></div>
<input id='result' placeholder='Result'>
<textarea id='lesson' placeholder='Lesson'></textarea>
<button onclick='updateTrade()'>Save Post-Trade</button></div>

<div class='card'><h3>Recent Trades</h3><button onclick='loadTrades()'>Refresh</button><div id='list'></div></div>
<script>
async function api(path, opts={}){const r=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});return r.json();}
async function createTrade(){
 const body={symbol:v('symbol'),chain:v('chain'),side:v('side'),entry:num('entry'),size_usd:num('size'),conviction:num('conv'),thesis:v('thesis'),invalidation:v('inv')};
 const j=await api('/api/trades',{method:'POST',body:JSON.stringify(body)}); alert('Created #'+j.id); loadTrades();
}
async function updateTrade(){
 const id=num('tid');
 const body={status:v('status'),exit:num('exit'),pnl_usd:num('pnl'),result:v('result'),lesson:v('lesson')};
 const j=await api('/api/trades/'+id,{method:'PUT',body:JSON.stringify(body)}); alert(j.ok?'Updated':'Not found'); loadTrades();
}
async function loadTrades(){
 const j=await api('/api/trades');
 const rows=j.rows||[];
 let html='<table><tr><th>ID</th><th>Pair</th><th>Side</th><th>Status</th><th>PnL</th><th>Conv</th></tr>';
 rows.forEach(r=>html+=`<tr><td>${r.id}</td><td>${r.symbol}/${r.chain}</td><td>${r.side}</td><td>${r.status}</td><td>${r.pnl_usd??''}</td><td>${r.conviction??''}</td></tr>`);
 html+='</table>'; document.getElementById('list').innerHTML=html;
}
function v(id){return document.getElementById(id).value}
function num(id){const x=parseFloat(v(id)); return isNaN(x)?null:x}
loadTrades();
</script></body></html>'''


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS trades (
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
        lesson TEXT
    )''')
    con.commit(); con.close()

class H(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        p = urlparse(self.path).path
        if p == '/':
            b = HTML.encode(); self.send_response(200); self.send_header('Content-Type','text/html'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b); return
        if p == '/api/trades':
            con=sqlite3.connect(DB_PATH); con.row_factory=sqlite3.Row; cur=con.cursor();
            cur.execute('SELECT id,symbol,chain,side,status,pnl_usd,conviction,created_at FROM trades ORDER BY id DESC LIMIT 100');
            rows=[dict(r) for r in cur.fetchall()]; con.close(); return self._json(200, {'rows': rows})
        self._json(404, {'error':'not found'})

    def do_POST(self):
        if urlparse(self.path).path != '/api/trades': return self._json(404, {'error':'not found'})
        ln=int(self.headers.get('Content-Length','0')); data=json.loads(self.rfile.read(ln) or '{}')
        con=sqlite3.connect(DB_PATH); cur=con.cursor(); ts=now_iso()
        cur.execute('''INSERT INTO trades (created_at,updated_at,symbol,chain,side,entry,size_usd,status,conviction,thesis,invalidation)
            VALUES (?,?,?,?,?,?,?,'open',?,?,?)''',
            (ts,ts,(data.get('symbol') or '').upper(),data.get('chain'),data.get('side'),data.get('entry'),data.get('size_usd'),data.get('conviction'),data.get('thesis'),data.get('invalidation')))
        tid=cur.lastrowid; con.commit(); con.close(); self._json(200, {'id': tid})

    def do_PUT(self):
        p=urlparse(self.path).path
        if not p.startswith('/api/trades/'): return self._json(404, {'error':'not found'})
        tid=int(p.split('/')[-1]); ln=int(self.headers.get('Content-Length','0')); data=json.loads(self.rfile.read(ln) or '{}')
        con=sqlite3.connect(DB_PATH); cur=con.cursor();
        cur.execute('''UPDATE trades SET updated_at=?, status=COALESCE(?,status), exit=COALESCE(?,exit), pnl_usd=COALESCE(?,pnl_usd), result=COALESCE(?,result), lesson=COALESCE(?,lesson) WHERE id=?''',
            (now_iso(), data.get('status'), data.get('exit'), data.get('pnl_usd'), data.get('result'), data.get('lesson'), tid))
        ok=cur.rowcount>0; con.commit(); con.close(); self._json(200, {'ok': ok})

if __name__ == '__main__':
    init_db()
    print(f'Trade Diary app running on http://{HOST}:{PORT}')
    HTTPServer((HOST, PORT), H).serve_forever()
