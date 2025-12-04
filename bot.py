import ccxt
import time

# === YOUR REAL KEYS (keep these safe!) ===
exchange = ccxt.binance({
    'apiKey': 'GSLsR8fTMcr4mGNJXzDySqHQBNIhljuVLjmZCGPp8Ehrd1jvyRdsmTsaeG56XjiS',
    'secret': 'uJQLBtlCJ4Wftfvc4ixhOMZh7eMoillAEhyesey1eAPcEucKAwbtAVku1puAgNbi',
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

symbol = 'SOL/USDT'      # we only trade SOL
trade_usdt = 6                  # $6 per trade (safe for your balance)

print("SOL Smart Bot LIVE – Ctrl+C to stop anytime")
print("Strategy: Buy ≤ $138  |  Sell ≥ $143  |  $6 per trade")

while True:
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        print(f"\n{time.strftime('%Y-%m-%d %H:%M')}  |  SOL = ${price:.2f}")

        balance = exchange.fetch_balance()
        usdt = balance['total'].get('USDT', 0) + balance['total'].get('USDC', 0)
        sol  = balance['total'].get('SOL', 0)

        print(f"   USDT available: {usdt:.2f}  |  SOL holding: {sol:.5f}")

        # === BUY on dip ===
        if price <= 138 and usdt >= trade_usdt + 2:
            amount_sol = trade_usdt / price
            order = exchange.create_market_buy_order(symbol, amount_sol)
            print(f"   BOUGHT {amount_sol:.4f} SOL at ${price:.2f} ")

        # === SELL on pump ===
        if price >= 143 and sol >= 0.01:           # have at least ~$1.40 of SOL
            sell_sol = sol * 0.60                   # sell 60%, keep 40% for next dip
            order = exchange.create_market_sell_order(symbol, sell_sol)
            profit_usdt = sell_sol * price
            print(f"   SOLD {sell_sol:.4f} SOL at ${price:.2f} → +${profit_usdt:.2f}")

        time.sleep(60)  # check every minute

    except Exception as e:
        print("Small error (normal):", e)
        time.sleep(60)