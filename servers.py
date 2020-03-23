

from typing import Optional
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Optional
import re
from collections import Counter



class Product:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
    def __hash__(self):
        return hash((self.name, self.price))

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

class TooManyProductsFoundError(Exception):

    pass

class Server(ABC):
    def __init__(self,list_prod: List[Product]):
        self.list_prod = list_prod

    def to_dict(self)->Dict[Product,str]:
        slownik = {}
        for elem in self.list_prod:
            slownik[elem.name] = elem
        return slownik

    n_max_returned_entries = 5


    @abstractmethod
    def get_entries(self, n_letters:int = 1):
        pass



class ListServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = self.list_prod

    def get_entries(self, n_letters:int )->List[Product]:
        geted_prod = []
        for elem in self.list_prod:
            m = re.match(r"(?P<letters>[a-zA-Z]+)(?P<the_rest>.+)$", elem.name)

            if len(m.groups()[0]) == n_letters and 2<=len(m.groups()[1])<=3:
                geted_prod.append(elem)

        if len(geted_prod) == 0:
            return []

        if len(geted_prod) > self.n_max_returned_entries:
            raise TooManyProductsFoundError()

        return sorted(geted_prod, key=lambda product: product.price)






class MapServer(Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = self.to_dict()


    def get_entries(self, n_letters:int )->List[Product]:
        geted_prod = []
        for elem in self.products.keys():
            m = re.match(r"(?P<letters>[a-zA-Z]+)(?P<the_rest>.+)$", elem)
            if m:
                if len(m.groups()[0]) == n_letters and 2<=len(m.groups()[1])<=3:
                    geted_prod.append(self.products[elem])

        if len(geted_prod) == 0:
            return []

        if len(geted_prod) > self.n_max_returned_entries:
            raise TooManyProductsFoundError()

        return sorted(geted_prod, key=lambda product: product.price)


class Client:

    def __init__(self,server :Server):
        self.server = server
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            entries = self.server.get_entries(n_letters)

        except TooManyProductsFoundError:
            return None

        if len(entries) == 0:
            return None

        entries_price = 0
        for entry in entries:
            entries_price += entry.price
        return entries_price


