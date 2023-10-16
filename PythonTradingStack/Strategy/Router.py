##CLASS: ROUTER
"""
def __init__(client, sell_token, buy_token):
    self.client=client
    self.symbol, self.direction = trading_pair_exists()

"""

## 1 Convert format (sell_token, buy_token) into (pair, direction)
#TO:DO make this search multiple jumps
def trading_pair_exists(client, sell_token, buy_token):
    """
    Check if a trading pair exists between two tokens.
    
    :param client: Binance client object
    :param asset_X: First token (e.g., 'BTC')
    :param asset_Y: Second token (e.g., 'USDT')
    :return: Tuple containing the valid trading pair and its direction, or (None, None) if no valid pair is found
    """
    exchange_info = client.get_exchange_info()
    trading_pairs = [s['symbol'] for s in exchange_info['symbols']]
    
    if (sell_token + buy_token) in trading_pairs:
        return (sell_token + buy_token, 'SELL')
    elif (buy_token + sell_token) in trading_pairs:
        return (buy_token + sell_token, 'BUY')
    else:
        print("Trade pair not found")
        return (None, None)
    

## 2 Get historical price
#TO-DO get_hourly_avg_price(sell_token, buy_token, sell_size) --> buy_output_quantity && buy_output_price
def get_hourly_avg_price(symbol):
    # Get the klines (candlestick data) for the past hour at 1-minute intervals
    klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=60)

    # Extract the close prices from the klines
    close_prices = [float(kline[4]) for kline in klines]

    # Calculate the average price over the last hour
    avg_price = sum(close_prices) / len(close_prices)

    return avg_price


## 3 Estimate price output
#TO-DO get_average_execution_price(sell_token, buy_token, sell_size) --> buy_output_quantity && buy_output_price
def get_average_execution_price(client, symbol, order_size, side):

    """
    Estimate the average execution price per unit of a market order.
    
    :param client: Binance client object
    :param symbol: Symbol of the trading pair (e.g., 'BTCUSDT')
    :param order_size: Size of the order to estimate price impact for
    :param side: Either 'BUY' or 'SELL'
    :return: Estimated average execution price per unit
    """
    # Get the order book
    order_book = client.get_order_book(symbol=symbol, limit=1000)
    orders = order_book['asks'] if side == 'BUY' else order_book['bids']

    cumulative_volume = 0
    weighted_sum = 0

    for price, volume in orders:
        price = float(price)
        volume = float(volume)
        
        # Check if the volume at this level is enough to fill the remaining order
        if cumulative_volume + volume > order_size:
            volume_to_use = order_size - cumulative_volume
        else:
            volume_to_use = volume
        
        weighted_sum += volume_to_use * price
        cumulative_volume += volume_to_use

        if cumulative_volume >= order_size:
            break

    assert(cumulative_volume==order_size, f"{side}:{order_size} too big. Reached end of orderbook stack")
    average_price = weighted_sum / order_size
    return average_price

## 4 Get best route 
def best_route():
    route, direction = trading_pair_exists(client, sell_token, buy_token)
    assert(route and direction, "route not found")
    return route