
from dataclasses import dataclass

@dataclass
class ProductModel:
    id: str
    productIdAsString: str
    name: str
    fullname: str
    simpleName: str
    price: float
    insteadOfPrice: float