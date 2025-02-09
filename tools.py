from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

@dataclass
class Product:
    id: str
    name: str
    price: float
    color: str
    size: str
    store: str
    in_stock: bool

@dataclass
class ShippingDetails:
    cost: float
    estimated_delivery: datetime
    is_feasible: bool
    carrier: str

@dataclass
class ReturnPolicy:
    store: str
    duration_days: int
    free_returns: bool
    conditions: str

class FashionShoppingTools:
    def __init__(self):
        # Mock product database
        self.products = [
            Product("sk1", "Floral A-Line Skirt", 35.99, "blue", "S", "FashionCo", True),
            Product("sk2", "Denim Mini Skirt", 45.99, "blue", "S", "StyleHub", True),
            Product("sn1", "Classic White Sneakers", 65.99, "white", "8", "ShoeMart", True),
            Product("jk1", "Casual Denim Jacket", 79.99, "blue", "M", "SiteA", True),
            Product("jk2", "Casual Denim Jacket", 72.99, "blue", "M", "SiteB", True),
            Product("dr1", "Evening Cocktail Dress", 89.99, "black", "M", "SiteB", True),
        ]
        
        # Mock promo codes
        self.promo_codes = {
            "SAVE10": 0.10,
            "SUMMER20": 0.20,
            "FLASH15": 0.15
        }
        
        # Mock return policies
        self.return_policies = {
            "SiteA": ReturnPolicy("SiteA", 30, True, "Items must be unworn with original tags"),
            "SiteB": ReturnPolicy("SiteB", 14, False, "Return shipping fee applies"),
            "FashionCo": ReturnPolicy("FashionCo", 60, True, "Free returns within 60 days"),
            "StyleHub": ReturnPolicy("StyleHub", 30, True, "Full refund available"),
            "ShoeMart": ReturnPolicy("ShoeMart", 45, True, "Shoes must be unworn")
        }

    def search_products(
        self,
        query: str,
        max_price: Optional[float] = None,
        color: Optional[str] = None,
        size: Optional[str] = None
    ) -> List[Product]:
        """Search for products matching the given criteria."""
        results = []
        
        for product in self.products:
            if (query.lower() in product.name.lower() and
                (max_price is None or product.price <= max_price) and
                (color is None or color.lower() == product.color.lower()) and
                (size is None or size.lower() == product.size.lower())):
                results.append(product)
                
        return results

    def estimate_shipping(
        self,
        product: Product,
        target_date: Optional[datetime] = None
    ) -> ShippingDetails:
        """Estimate shipping details for a product."""
        base_shipping = 8.99
        standard_days = random.randint(3, 7)
        
        estimated_delivery = datetime.now() + timedelta(days=standard_days)
        is_feasible = True if target_date is None else estimated_delivery <= target_date
        
        return ShippingDetails(
            cost=base_shipping,
            estimated_delivery=estimated_delivery,
            is_feasible=is_feasible,
            carrier="FastShip"
        )

    def apply_discount(self, price: float, promo_code: str) -> Optional[float]:
        """Apply a discount code to the given price."""
        if promo_code in self.promo_codes:
            discount = self.promo_codes[promo_code]
            return price * (1 - discount)
        return None

    def compare_prices(self, product_name: str) -> List[Dict]:
        """Compare prices for a product across different stores."""
        results = []
        for product in self.products:
            if product_name.lower() in product.name.lower():
                results.append({
                    "store": product.store,
                    "price": product.price,
                    "in_stock": product.in_stock
                })
        return results

    def get_return_policy(self, store: str) -> Optional[ReturnPolicy]:
        """Get return policy details for a specific store."""
        return self.return_policies.get(store)