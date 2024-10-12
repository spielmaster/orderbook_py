import orderbook
import matplotlib.pyplot as plt
import pandas as pd

def depth_chart(orderbook_ : orderbook.Orderbook):
    
    sorted_bids = sorted(orderbook_.sides['bid'].keys())
    bids_and_volumes = dict(zip(sorted_bids, [orderbook_.sides['bid'][bid].get_level_volume() for bid in sorted_bids]))

    sorted_asks = sorted(orderbook_.sides['ask'].keys())
    asks_and_volumes = dict(zip(sorted_asks, [orderbook_.sides['ask'][ask].get_level_volume() for ask in sorted_asks]))

    to_plot_df = pd.DataFrame.from_dict({**bids_and_volumes, **asks_and_volumes}, orient = 'index', columns = ['volumes'])

    plt.plot(to_plot_df)
    plt.xlabel('price ($)')
    plt.ylabel('volume')
    plt.title('depth chart')
    plt.show()
