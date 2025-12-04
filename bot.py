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

# === ADD OR REMOVE COINS HERE (super easy) ===
coins = [
    {"symbol": "SOL/USDT",  "buy": 138,  "sell": 143,  "size_usdt": 6},
    {"symbol": "BNB/USDT",  "buy": 605,  "sell": 618,  "size_usdt": 6},
    {"symbol": "PEPE/USDT", "buy": 0.000022, "sell": 0.0000245, "size_usdt": 5},
    # ← add more lines like this if you want
]

print("Multi-Coin Bot LIVE 24/7 – Trading", len(coins), "pairs")

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

                print(f"{time.strftime('%H:%M')} | {symbol:12} ${price:.6f} | USDT {usdt:.2f} | {base} {base_amount:.6f}")

                # BUY
                if price <= coin["buy"] and usdt >= coin["size_usdt"] + 2:
                    amount = coin["size_usdt"] / price
                    exchange.create_market_buy_order(symbol, amount)
                    print(f"   BOUGHT {amount:.6f} {base} @ ${price}")

                # SELL 60%
                if price >= coin["sell"] and base_amount >= 0.0001:
                    sell_amt = base_amount * 0.6
                    exchange.create_market_sell_order(symbol, sell_amt)
                    print(f"   SOLD {sell_amt:.6f} {base} @ ${price} → PROFIT")

            print("-" * 60)
            time.sleep(60)

        except Exception as e:
            print("Error:", e)
            time.sleep(60)

# Run bot in background
import threading
threading.Thread(target=run_bot, daemon=True).start()

# Dummy web page (keeps Render alive)
@app.route('/')
def home():
    return "Multi-Coin Bot Running<br>Trading: " + ", ".join(c["symbol"] for c in coins)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
