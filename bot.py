import ccxt
import time
import os
from flask import Flask

app = Flask(__name__)

exchange = ccxt.binance({
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('API_SECRET'),
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

# 5 COINS – DECEMBER 2025 EDITION
coins = [
    {"symbol": "SOL/USDT",   "buy": 138.0,   "sell": 143.0,   "size_usdt": 6},
    {"symbol": "BNB/USDT",   "buy": 605.0,   "sell": 618.0,   "size_usdt": 6},
    {"symbol": "PEPE/USDT",  "buy": 0.0000220, "sell": 0.0000245, "size_usdt": 5},
    {"symbol": "DOGE/USDT",  "buy": 0.365,   "sell": 0.395,   "size_usdt": 5},
    {"symbol": "XRP/USDT",   "buy": 2.18,    "sell": 2.38,    "size_usdt": 6},
]

print("5-Coin Monster Bot LIVE 24/7 – Trading SOL • BNB • PEPE • DOGE • XRP")

def run_bot():
    while True:
        try:
            for coin in coins:
                symbol = coin["symbol"]
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']

                balance = exchange.fetch_balance()
                usdt = balance['total'].get('USDT', 0) + balance['total'].get('USDC', 0)
                base = symbol.split('/')[0]
                base_amount = balance['total'].get(base, 0)

                print(f"{time.strftime('%H:%M')} | {symbol:12} ${price:.7f} | USDT {usdt:.2f} | {base} {base_amount:.6f}")

                # BUY
                if price <= coin["buy"] and usdt >= coin["size_usdt"] + 2:
                    amount = coin["size_usdt"] / price
                    exchange.create_market_buy_order(symbol, amount)
                    print(f"   BOUGHT {amount:.6f} {base} @ ${price:.7f}")

                # SELL 60%
                if price >= coin["sell"] and base_amount * price >= 1.0:
                    sell_amt = base_amount * 0.6
                    exchange.create_market_sell_order(symbol, sell_amt)
                    print(f"   SOLD {sell_amt:.6f} {base} @ ${price:.7f} → PROFIT!")

            print("-" * 70)
            time.sleep(60)

        except Exception as e:
            print("Error (retrying):", e)
            time.sleep(60)

import threading
threading.Thread(target=run_bot, daemon=True).start()

@app.route('/')
def home():
    return "5-Coin Monster Bot Running 24/7<br>Trading: SOL • BNB • PEPE • DOGE • XRP"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
