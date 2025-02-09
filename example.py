from tools import FashionShoppingTools
from agent import FashionShoppingAgent

# Example usage
agent = FashionShoppingAgent()

# Task A: Basic Item Search + Price Constraint
print("Task A:")
query_a = "Find a floral skirt under $40 in size S. Is it in stock, and can I apply a discount code 'SAVE10'?"
print(agent.process_query(query_a))

# Task B: Shipping Deadline
print("\nTask B:")
query_b = "I need white sneakers (size 8) for under $70 that can arrive by Friday."
print(agent.process_query(query_b))

# Task C: Competitor Price Comparison
print("\nTask C:")
query_c = "I found a 'casual denim jacket' at $80 on SiteA. Any better deals?"
print(agent.process_query(query_c))

# Task D: Returns & Policies
print("\nTask D:")
query_d = "I want to buy a cocktail dress from SiteB, but only if returns are hassle-free. Do they accept returns?"
print(agent.process_query(query_d))