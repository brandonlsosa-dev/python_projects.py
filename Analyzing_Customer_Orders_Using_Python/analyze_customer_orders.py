"""Analyzing customer orders with clearer structure and small optimizations.

This script preserves the original analysis but organizes logic into functions
so it is easier to test and reuse.
"""

from collections import defaultdict, Counter
from typing import List, Tuple, Dict, Set

Order = Tuple[str, str, float, str]


ORDER_DETAILS: List[Order] = [
    ('Alice', 'Laptop', 850, 'Electronics'),
    ('Bob', 'T-shirt', 25, 'Clothing'),
    ('Charlie', 'Vacuum Cleaner', 120, 'Home Essentials'),
    ('Diana', 'Smartphone', 700, 'Electronics'),
    ('Ethan', 'Jeans', 55, 'Clothing'),
    ('Fiona', 'Blender', 45, 'Home Essentials'),
    ('Grace', 'Headphones', 90, 'Electronics'),
    ('Henry', 'Jacket', 80, 'Clothing'),
    ('Isabella', 'Air Purifier', 150, 'Home Essentials'),
    ('Jacob', 'Smartwatch', 200, 'Electronics'),
]


def analyze_orders(orders: List[Order]) -> Tuple[Dict[str, Dict[str, object]], Dict[str, float], Dict[str, Set[str]], Dict[str, List[str]], Dict[str, str]]:
    """Return several derived structures from the raw orders list.

    Returns:
        customer_analysis: Dict[name, {'Total Spent': float, 'Classification': str}]
        customer_spending: Dict[name, total_spent]
        customer_categories: Dict[name, Set[categories]]
        customer_orders: Dict[name, List[products]]
        product_to_category: Dict[product, category]
    """
    customer_spending: Dict[str, float] = defaultdict(float)
    customer_categories: Dict[str, Set[str]] = defaultdict(set)
    customer_orders: Dict[str, List[str]] = defaultdict(list)
    product_to_category: Dict[str, str] = {}

    for name, product, price, category in orders:
        customer_spending[name] += price
        customer_categories[name].add(category)
        customer_orders[name].append(product)
        product_to_category[product] = category

    customer_analysis: Dict[str, Dict[str, object]] = {}
    for name, total in customer_spending.items():
        if total > 100:
            classification = "high-value buyer"
        elif 50 <= total <= 100:
            classification = "moderate buyer"
        else:
            classification = "low-value buyer"

        customer_analysis[name] = {
            'Total Spent': total,
            'Classification': classification,
        }

    return (
        customer_analysis,
        dict(customer_spending),
        {k: set(v) for k, v in customer_categories.items()},
        dict(customer_orders),
        product_to_category,
    )


def category_revenue(orders: List[Order]) -> Dict[str, float]:
    """Compute total revenue per category using Counter for efficiency."""
    rev: Counter = Counter()
    for _, _, price, category in orders:
        rev[category] += price
    return dict(rev)


def unique_products(orders: List[Order]) -> Set[str]:
    return {product for _, product, _, _ in orders}


def customers_by_category(orders: List[Order], category_name: str) -> List[str]:
    return sorted({name for name, _, _, category in orders if category == category_name})


def top_n_customers(customer_spending: Dict[str, float], n: int = 3) -> List[Tuple[str, float]]:
    # For small n, sorting is fine; keep simple and predictable
    return sorted(customer_spending.items(), key=lambda t: t[1], reverse=True)[:n]


def main():
    print("--- Step 1: Store Customer Orders ---")
    customer_names = sorted({name for name, *_ in ORDER_DETAILS})
    print("Customer Names List:", customer_names)
    print("Number of Orders Stored:", len(ORDER_DETAILS))

    (
        customer_analysis,
        customer_spending,
        customer_categories,
        customer_orders,
        product_to_category,
    ) = analyze_orders(ORDER_DETAILS)

    print("\n--- Step 2: Classify Products by Category ---")
    print("Product to Category Mapping (sample):", dict(list(product_to_category.items())[:5]))
    unique_categories_set = set(product_to_category.values())
    print("Unique Product Categories (Set):", unique_categories_set)

    print("\n--- Step 3: Analysis Summary (Customer Classification) ---")
    header = f"{'Customer': <10} | {'Product': <18} | {'Price': <5} | {'Category': <16} | Classification"
    print(header)
    print("-" * len(header))
    for name, product, price, category in ORDER_DETAILS:
        classification = customer_analysis[name]['Classification']
        print(f"{name: <10} | {product: <18} | ${price: <4} | {category: <16} | {classification}")

    print("\n--- Step 4: Business Insights ---")
    rev = category_revenue(ORDER_DETAILS)
    print("4.1 Total Revenue per Product Category (Dictionary):", rev)
    print("4.2 Unique Products Purchased (Set):", unique_products(ORDER_DETAILS))
    print("4.3 Customers who purchased Electronics (List Comprehension):", customers_by_category(ORDER_DETAILS, 'Electronics'))
    print("4.4 Top three highest-spending customers (Sorting):")
    for customer, total in top_n_customers(customer_spending, 3):
        print(f"- {customer}: ${total:.2f}")

    print("\n--- Step 5: Organized Display ---")
    print("\n5.1 Summary of Customer Spending and Classification:")
    print(f"{'Customer': <10} | {'Total Spent': <11} | Classification")
    print("-" * 45)
    for name, details in customer_analysis.items():
        print(f"{name: <10} | ${details['Total Spent']: <10.2f} | {details['Classification']}")

    multi_category_customers = [n for n, cats in customer_categories.items() if len(cats) > 1]
    print("\n5.2 Customers Who Purchased from Multiple Categories (Set Operation):")
    print(multi_category_customers)

    electronics_buyers = {n for n, _, _, c in ORDER_DETAILS if c == 'Electronics'}
    clothing_buyers = {n for n, _, _, c in ORDER_DETAILS if c == 'Clothing'}
    common = electronics_buyers & clothing_buyers
    print("\n5.3 Common Customers (Electronics AND Clothing) (Set Intersection):")
    print(common)


if __name__ == '__main__':
    main()