import utils.ip as ip 
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

#TEST API keys
api_key="E0diYeGVd7bDe0myC6iaXYth3JqY073ywb10xMn42ggILqUVWUEfDGpFPQPGOSkp" 
api_secret="V5XBuUxkLrVGgOplAwVMChQQT7K5FcwwJnnfY0AAEccOsklTlq4AaUJI2aTNy5Id"

#print(ip.info())
assert(ip.get_city()=="São Paulo", "Ensure VPN is connected to BR-9")


#
from Strategy.Router import get_average_execution_price
client = Client(api_key, api_secret, testnet=True)

#Say we want to get the output price from selling 1m USDC to USDT  on this pair https://www.binance.com/en/trade/USDC_USDT?type=spot
order_pair='USDCUSDT'
order_size=10
direction='SELL' #See CLOB defintion of asset and quote. Buy means buying USDC and sell means selling USDC.



#Option 1) We can return the orderbook directly
order_book = client.get_order_book(symbol=order_pair, limit=1000)
print(order_book)

#Option 2) We can get the output price directly 
average_price=get_average_execution_price(client, order_pair, order_size, direction)
print(average_price)