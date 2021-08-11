import math
import time
import upbit
import analyzer

K = 1 + 0.04
MIN_PRICE = 6000
DAYS = 3
RATES = -3

while True:
    account = upbit.get_my_account()
    print('')
    print(account)
    money = math.trunc(float(account['KRW']['balance']))

    if money < MIN_PRICE:
        time.sleep(30)
        continue

    coins = upbit.get_KRW_coins()

    candidates = []

    for coin, name in coins:
        candles = upbit.get_coin_candle(coin, count=DAYS)
        can_i_candidate, rate, price = analyzer.check_candidate(candles)

        if can_i_candidate:
            candidates.append([coin, name, price, rate])

        time.sleep(0.1)

    candidates = sorted(candidates, key=lambda x: x[2])
    print(candidates)

    target_money = 13000

    if money < target_money:
        target_money = money

    for id, name, price, rate in candidates:
        coin_id = id.split('-')[1]

        if coin_id in account or rate > RATES: # or price > 1200:
            continue

        count = target_money / price

        if count * price < MIN_PRICE:
            break

        print("{}'s price: {}, count: {}".format(id, price, count))
        order_uuid = upbit.buy_coin(id, price, count)

        order_status = False

        for _ in range(5):
            time.sleep(10)
            order_status = upbit.get_order_status(order_uuid)

            if order_status == True:
                time.sleep(3)
                target_price = round(price * K, -1) if price > 2000 else math.ceil(price * K)
                upbit.sell_coin(id, target_price, count)
                print('uuid: {} is ok, target_price: {}'.format(order_uuid, target_price))
                break

        if not order_status:
            upbit.cancel_order(order_uuid)
            print('uuid: {} is cancelled'.format(order_uuid))
        else:
            break

    time.sleep(60)