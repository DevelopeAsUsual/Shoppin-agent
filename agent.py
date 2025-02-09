from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from tools import FashionShoppingTools, Product

class FashionShoppingAgent:
    def __init__(self):
        self.tools = FashionShoppingTools()
        
    def _parse_price_constraint(self, query: str) -> Optional[float]:
        """Extract price constraint from query."""
        if "under" in query.lower():
            words = query.split()
            for i, word in enumerate(words):
                if word.lower() == "under" and i + 1 < len(words):
                    try:
                        return float(words[i + 1].replace("$", ""))
                    except ValueError:
                        pass
        return None

    def _parse_size(self, query: str) -> Optional[str]:
        """Extract size information from query."""
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() == "size" and i + 1 < len(words):
                return words[i + 1]
        return None

    def _extract_promo_code(self, query: str) -> Optional[str]:
        """Extract promo code from query."""
        if "'" in query:
            try:
                return query.split("'")[1]
            except IndexError:
                pass
        return None

    def process_query(self, query: str) -> str:
        """Process a user query and return a response."""
        query = query.lower()
        response_parts = []

        # Task A: Basic Item Search + Price Constraint
        if "find" in query or "search" in query:
            max_price = self._parse_price_constraint(query)
            size = self._parse_size(query)
            promo_code = self._extract_promo_code(query)
            
            products = self.tools.search_products(
                query=query,
                max_price=max_price,
                size=size
            )
            
            if not products:
                return "I couldn't find any products matching your criteria."
                
            response_parts.append("Here's what I found:")
            for product in products:
                response = f"\n- {product.name} (${product.price:.2f}) in size {product.size}"
                if product.in_stock:
                    response += " - In Stock"
                    
                    if promo_code:
                        discounted_price = self.tools.apply_discount(product.price, promo_code)
                        if discounted_price:
                            response += f"\n  With promo code '{promo_code}': ${discounted_price:.2f}"
                        else:
                            response += f"\n  Promo code '{promo_code}' is invalid"
                            
                response_parts.append(response)

        # Task B: Shipping Deadline
        if "arrive by" in query or "delivery" in query:
            # Parse target date (simplified for demo)
            target_date = datetime.now() + timedelta(days=5)  # Assuming "Friday" is 5 days away
            
            products = self.tools.search_products(query=query)
            if products:
                for product in products:
                    shipping = self.tools.estimate_shipping(product, target_date)
                    response = f"\nShipping for {product.name}:"
                    response += f"\n- Estimated delivery: {shipping.estimated_delivery.strftime('%A, %B %d')}"
                    response += f"\n- Shipping cost: ${shipping.cost:.2f}"
                    response += f"\n- Delivery by target date: {'Yes' if shipping.is_feasible else 'No'}"
                    response_parts.append(response)

        # Task C: Competitor Price Comparison
        if "better deals" in query or "compare" in query:
            if "jacket" in query:  # Example for denim jacket
                comparisons = self.tools.compare_prices("Casual Denim Jacket")
                response_parts.append("\nPrice comparison for Casual Denim Jacket:")
                for comp in comparisons:
                    response_parts.append(f"- {comp['store']}: ${comp['price']:.2f}")

        # Task D: Returns & Policies
        if "return" in query:
            store = None
            for potential_store in ["SiteA", "SiteB", "FashionCo", "StyleHub", "ShoeMart"]:
                if potential_store.lower() in query.lower():
                    store = potential_store
                    break
                    
            if store:
                policy = self.tools.get_return_policy(store)
                if policy:
                    response_parts.append(f"\nReturn Policy for {store}:")
                    response_parts.append(f"- Duration: {policy.duration_days} days")
                    response_parts.append(f"- Free returns: {'Yes' if policy.free_returns else 'No'}")
                    response_parts.append(f"- Conditions: {policy.conditions}")

        return "\n".join(response_parts) if response_parts else "I'm sorry, I couldn't understand your request."