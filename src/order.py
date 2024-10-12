import dataclasses
import random

@dataclasses.dataclass
class Order:
    side: str
    price: float
    initial_qty: int

    def __post_init__(self):
        self.ID: str = f'{self.side}_{str(self.price)}_{str(self.initial_qty)}_{str(random.randint(0, 999))}'
        self.remaining_quantity: float = self.initial_qty

    def get_filled_quantity(self):
        return self.initial_qty - self.remaining_quantity

    def fill(self, fill_qty: float) -> float:
        
        if fill_qty > self.remaining_quantity:
            # to do raise exception
            print('cannot fill more than order quantity')
        self.remaining_quantity -= fill_qty

    def is_filled(self) -> bool: 
        return self.remaining_quantity == 0
    
@dataclasses.dataclass
class GoodTillCanceled(Order):
    pass

@dataclasses.dataclass
class FillAndKillOrder(Order):
    pass
