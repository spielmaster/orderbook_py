import dataclasses
import collections
import order

@dataclasses.dataclass 
class OrdersQueue:

    #fifo
    queue: list = dataclasses.field(default_factory=list)

    def push_order(self, new_order: order.Order) -> None:
        self.queue.append(new_order)

    def is_empty(self):
        return not bool(len(self.queue))

    def get_level_volume(self) -> int:
        if self.is_empty():
            return 0
        return sum([order_.remaining_quantity for order_ in self.queue])

    def _find_order(self, order_id: str) -> int | None:

        if not self.queue:
            return None
        
        return self.queue.index(order_id)

    def cancel_order(self, order_id: str) -> None:
        pass

@dataclasses.dataclass
class Orderbook:

    sides = {
        'bid': collections.OrderedDict(),
        'ask': collections.OrderedDict()
    }

    order_map = collections.OrderedDict()
    
    def clean_price_level(self, side: str, price: float) -> None:

        if self.sides[side][price].is_empty():
            self.sides[side][price].pop(price, None)
            
    def receive_new_order(self, new_order: order.Order) -> int:
        
        def order_codes(action: str):

            codes = {
                'error': 0,
                'killed': 1,
                'posted': 2,
                'partially_filled_and_posted': 3,
                'totally_filled': 4,
                'cancelled': 5, 
            }

            return codes[action] if action in codes else codes['error']

        # try to match
        if self._can_match_order(new_order.side, new_order.price):
            action = self.match_order(new_order)
            return order_codes(action = action)

        # kill if fill and kill
        if isinstance(new_order, order.FillAndKillOrder):
            return order_codes(action = 'killed')
        
        # post
        action = self._post_order(new_order)

        pass

    def _can_match_order(self, side: str, price: float) -> bool:

        if side == 'bid':
            if not self.sides['ask']:
                return False
            return price >= self.get_best_ask()
            
        if side == 'ask':
            if not self.sides['bid']:
                return  False
            return price <= self.get_best_bid()

    def _match_order(self, side: str, price: float):

        pass

    def _post_order(self, new_order: order.Order) -> None:

        if new_order.price in self.sides[new_order.side]:
            self.sides[new_order.side][new_order.price].push_order(new_order)

        else:
            self.sides[new_order.side][new_order.price] = OrdersQueue()
            self.sides[new_order.side][new_order.price].push_order(new_order)

        self.order_map[new_order.ID] = new_order.price

    def fill_order(self):
        pass
    
    def get_total_bid_volume(self) -> int:

        if not self.sides['bid']:
            return 0

        return sum([self.sides['bid'][level].get_level_volume() for level in list((self.sides['bid'].keys()))])

    def get_total_ask_volume(self) -> int:

        if not self.sides['ask']:
            return 0
            
        return sum([self.sides['ask'][level].get_level_volume() for level in list((self.sides['ask'].keys()))])

    def get_best_bid_volume(self) -> int:
        if self.sides['bid']:

            best_bid = self.get_best_bid()
            return self.sides['bid'][best_bid].get_level_volume()

        return 0

    def get_best_ask_volume(self) -> int:
        if self.sides['ask']:

            best_ask = self.get_best_ask()
            return self.sides['ask'][best_ask].get_level_volume()

        return 0

    def get_best_ask(self) -> float | None:

        if self.sides['ask']:
            return min(list(self.sides['ask'].keys()))
        return None
        
    def get_best_bid(self) -> float | None:

        if self.sides['bid']:
            return max(list(self.sides['bid'].keys()))
        return None
        if self.sides['ask']:
            return max(list(self.sides['ask'].keys()))
        return None
