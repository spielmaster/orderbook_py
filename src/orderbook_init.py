import orderbook
import numpy as np
import order

def triangular_symmetrical(mid: float, top_spread: float, bottom_spread: float, 
                                    top_volume: int, bottom_volume: int, levels: int, 
                                    precision: int = 4, orderbook_: orderbook.Orderbook = None) -> None | orderbook.Orderbook:


    orderbook_ = orderbook_ if orderbook_ else orderbook.Orderbook()

    spreads = np.linspace(top_spread, bottom_spread, levels).round(4)
    volumes = np.linspace(top_volume, bottom_volume, levels).round(0)

    for level in range(levels):

        bid = mid - spreads[level]
        ask = mid + spreads[level]
        qty = volumes[level]

        bid_order = order.Order(side = 'bid', price = bid, initial_qty=qty)
        ask_order = order.Order(side = 'ask', price = ask, initial_qty=qty)

        orderbook_.receive_new_order(bid_order)
        orderbook_.receive_new_order(ask_order)
    
    return orderbook_
