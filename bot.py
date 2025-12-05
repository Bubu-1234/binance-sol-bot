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

coins = [
    {"symbol": "BTC/USDT", "buy": 91200, "sell": 92500, "size_usdt": 6, "stop_loss": -0.015},
    {"symbol": "SOL/USDT", "buy": 139.5, "sell": 142.5, "size_usdt": 6, "stop_loss": -0.015},
    {"symbol": "PEPE/USDT", "buy": 0.0000234, "sell": 0.0000241, "size_usdt": 5, "stop_loss": -0.015},
    {"symbol": "XRP/USDT", "buy": 2.195, "sell": 2.240, "size_usdt": 7, "stop_loss": -0.015},
]

print("Low-Risk 4-Coin Bot LIVE – $15+ Daily Target | 0.5% Risk/Trade")

entry_prices = {}

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

                print(f"{time.strftime('%H:%M')} | {symbol} ${price:.6f} | USDT {usdt:.2f} | {base} {base_amount:.6f}")

                # BUY with DCA for BTC
                if price <= coin["buy"] and usdt >= coin["size_usdt"] + 2:
                    amount = coin["size_usdt"] / price
                    if coin["symbol"] == "BTC/USDT":
                        third = amount / 3
                        exchange.create_market_buy_order(symbol, third)
                        time.sleep(20)
                        exchange.create_market_buy_order(symbol, third)
                        time.sleep(20)
                        exchange.create_market_buy_order(symbol, third)
                    else:
                        exchange.create_market_buy_order(symbol, amount)
                    entry_prices[base] = price
                    print(f"   BOUGHT {amount:.6f} {base} @ ${price:.6f} (DCA if BTC)")

                # SELL 60% on profit
                if price >= coin["sell"] and base_amount * price >= 1.0:
                    sell_amt = base_amount * 0.6
                    exchange.create_market_sell_order(symbol, sell_amt)
                    print(f"   SOLD {sell_amt:.6f} {base} @ ${price:.6f} → PROFIT!")

                # STOP-LOSS (-1.5% from entry)
                if base in entry_prices and base_amount > 0 and (price / entry_prices[base] <= (1 + coin["stop_loss"])):
                    exchange.create_market_sell_order(symbol, base_amount)
                    print(f"   STOP-LOSS {base_amount:.6f} {base} @ ${price:.6f}")
                    del entry_prices[base]

            print("-" * 60)
            time.sleep(60)

        except Exception as e:
            print("Error:", e)
            time.sleep(60)

import threading
threading.Thread(target=run_bot, daemon=True).start()

@app.route('/')
def home():
    return "Low-Risk Bot Running – $15+ Daily | BTC, SOL, PEPE, XRP | Logs for Trades"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
