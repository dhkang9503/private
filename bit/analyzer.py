def check_candidate(candles):
    candle_len = len(candles)

    minus_len = 0

    for candle in candles:
        delta = candle['trade_price'] - candle['opening_price']
        # print(candle['trade_price'], candle['opening_price'], delta)

        if delta < 0:
            minus_len += 1

    return candle_len == minus_len, (candles[0]['trade_price'] / candles[candle_len - 1]['opening_price'] * 100) - 100, candles[0]['trade_price']

def check_current_place(coins):
    total_len = len(coins)

    for coin in coins:
        print(coin)