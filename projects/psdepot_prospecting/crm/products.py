#!/usr/bin/env python3
"""
PSDEPOT Product & Service Catalog
Performance Supply Depot LLC
"""

PRODUCTS = {
    # Thermal Receipt Paper Products
    "thermal_roll_3x6": {
        "name": "Thermal Roll 3\" x 6\"",
        "description": "Premium thermal receipt paper rolls, 3 inch x 6 inch",
        "category": "thermal_paper",
        "unit": "case",
        "units_per_case": 50,
        "price_per_unit": 24.99,
        "min_order": 1,
        "sku": "TR-3x6-50",
        "keywords": ["receipt paper", "thermal roll", "POS", "register"]
    },
    "thermal_roll_3x7": {
        "name": "Thermal Roll 3\" x 7\"",
        "description": "Premium thermal receipt paper rolls, 3 inch x 7 inch",
        "category": "thermal_paper",
        "unit": "case",
        "units_per_case": 50,
        "price_per_unit": 26.99,
        "min_order": 1,
        "sku": "TR-3x7-50",
        "keywords": ["receipt paper", "thermal roll", "POS", "register"]
    },
    "thermal_roll_3x8": {
        "name": "Thermal Roll 3\" x 8\"",
        "description": "Premium thermal receipt paper rolls, 3 inch x 8 inch",
        "category": "thermal_paper",
        "unit": "case",
        "units_per_case": 50,
        "price_per_unit": 28.99,
        "min_order": 1,
        "sku": "TR-3x8-50",
        "keywords": ["receipt paper", "thermal roll", "POS", "register"]
    },
    "thermal_roll_4x6": {
        "name": "Thermal Roll 4\" x 6\"",
        "description": "Premium thermal receipt paper rolls, 4 inch x 6 inch",
        "category": "thermal_paper",
        "unit": "case",
        "units_per_case": 50,
        "price_per_unit": 29.99,
        "min_order": 1,
        "sku": "TR-4x6-50",
        "keywords": ["receipt paper", "thermal roll", "POS", "register"]
    },
    "thermal_roll_4x7": {
        "name": "Thermal Roll 4\" x 7\"",
        "description": "Premium thermal receipt paper rolls, 4 inch x 7 inch",
        "category": "thermal_paper",
        "unit": "case",
        "units_per_case": 50,
        "price_per_unit": 31.99,
        "min_order": 1,
        "sku": "TR-4x7-50",
        "keywords": ["receipt paper", "thermal roll", "POS", "register"]
    },
    "thermal_roll_4x8": {
        "name": "Thermal Roll 4\" x 8\"",
        "description": "Premium thermal receipt paper rolls, 4 inch x 8 inch",
        "category": "thermal_paper",
        "unit": "case",
        "units_per_case": 50,
        "price_per_unit": 33.99,
        "min_order": 1,
        "sku": "TR-4x8-50",
        "keywords": ["receipt paper", "thermal roll", "POS", "register"]
    },
    
    # Bond Paper
    "bond_8x11": {
        "name": "Bond Paper 8.5\" x 11\"",
        "description": "Standard letter size bond paper for receipts and invoices",
        "category": "paper",
        "unit": "case",
        "units_per_case": 5000,
        "price_per_unit": 45.99,
        "min_order": 1,
        "sku": "BP-8x11-5M",
        "keywords": ["bond paper", "copy paper", "letter size", "printer"]
    },
    "bond_8x14": {
        "name": "Bond Paper 8.5\" x 14\" (Legal)",
        "description": "Legal size bond paper for longer receipts",
        "category": "paper",
        "unit": "case",
        "units_per_case": 5000,
        "price_per_unit": 55.99,
        "min_order": 1,
        "sku": "BP-8x14-5M",
        "keywords": ["bond paper", "legal size", "printer"]
    },
    
    # Ink & Toner
    "toner_universal_black": {
        "name": "Universal Black Toner Cartridge",
        "description": "Compatible black toner for most laser printers",
        "category": "ink_toner",
        "unit": "each",
        "units_per_case": 1,
        "price_per_unit": 49.99,
        "min_order": 1,
        "sku": "TK-BLK-001",
        "keywords": ["toner", "black ink", "laser printer"]
    },
    "toner_universal_color": {
        "name": "Universal Color Toner Set (CMYK)",
        "description": "Compatible color toner set for laser printers",
        "category": "ink_toner",
        "unit": "set",
        "units_per_case": 4,
        "price_per_unit": 149.99,
        "min_order": 1,
        "sku": "TK-CLR-004",
        "keywords": ["toner", "color", "CMYK", "laser printer"]
    },
    "ink_cartridge_black": {
        "name": "Universal Black Ink Cartridge",
        "description": "Compatible black ink for inkjet printers",
        "category": "ink_toner",
        "unit": "each",
        "units_per_case": 1,
        "price_per_unit": 29.99,
        "min_order": 1,
        "sku": "IK-BLK-001",
        "keywords": ["ink", "black ink", "inkjet"]
    },
    
    # Point of Sale Supplies
    "pos_ribbon": {
        "name": "POS Printer Ribbon",
        "description": "Replacement ribbon for dot matrix POS printers",
        "category": "pos_supplies",
        "unit": "each",
        "units_per_case": 6,
        "price_per_unit": 18.99,
        "min_order": 1,
        "sku": "POS-RBN-006",
        "keywords": ["ribbon", "POS", "dot matrix", "printer"]
    },
    "cash_ribbon": {
        "name": "Cash Register Ribbon",
        "description": "Replacement ribbon for cash registers",
        "category": "pos_supplies",
        "unit": "each",
        "units_per_case": 6,
        "price_per_unit": 15.99,
        "min_order": 1,
        "sku": "CR-RBN-006",
        "keywords": ["ribbon", "cash register", "printer"]
    },
    "credit_card_paper": {
        "name": "Credit Card Slips (Carbonless)",
        "description": "Carbonless credit card imprint slips",
        "category": "pos_supplies",
        "unit": "pack",
        "units_per_case": 1000,
        "price_per_unit": 24.99,
        "min_order": 1,
        "sku": "CC-SLIP-1K",
        "keywords": ["credit card", "slips", "carbonless", "imprint"]
    },
    
    # Labels & Tags
    "shipping_labels_4x6": {
        "name": "Shipping Labels 4\" x 6\"",
        "description": "Direct thermal shipping labels, 4x6 inches",
        "category": "labels",
        "unit": "roll",
        "units_per_case": 500,
        "price_per_unit": 29.99,
        "min_order": 1,
        "sku": "LB-SHIP-500",
        "keywords": ["shipping", "labels", "4x6", "thermal"]
    },
    "price_labels_1x2": {
        "name": "Price Labels 1\" x 2\"",
        "description": "Direct thermal price labels, 1x2 inches",
        "category": "labels",
        "unit": "roll",
        "units_per_case": 3000,
        "price_per_unit": 12.99,
        "min_order": 1,
        "sku": "LB-PRICE-3K",
        "keywords": ["price labels", "thermal", "retail"]
    },
    "product_tags_2x4": {
        "name": "Product Tags 2\" x 4\"",
        "description": "Hang tags for products and inventory",
        "category": "labels",
        "unit": "pack",
        "units_per_case": 1000,
        "price_per_unit": 19.99,
        "min_order": 1,
        "sku": "TG-PROD-1K",
        "keywords": ["tags", "hang tags", "product", "inventory"]
    },
}

# Service offerings
SERVICES = {
    "setup_assist": {
        "name": "Printer Setup Assistance",
        "description": "Remote assistance with printer setup and configuration",
        "category": "service",
        "unit": "hour",
        "price_per_unit": 75.00,
        "min_order": 1,
        "sku": "SV-SETUP-01",
        "keywords": ["setup", "installation", "printer", "support"]
    },
    "bulk_discount": {
        "name": "Bulk Order Discount",
        "description": "Volume discount for orders over $500",
        "category": "discount",
        "unit": "order",
        "price_per_unit": 0,  # Percentage discount
        "discount_percent": 10,
        "min_order": 500,
        "sku": "DISC-BULK",
        "keywords": ["bulk", "discount", "volume"]
    },
    "rush_delivery": {
        "name": "Rush Delivery (1-2 Days)",
        "description": "Expedited shipping for urgent orders",
        "category": "service",
        "unit": "order",
        "price_per_unit": 35.00,
        "min_order": 1,
        "sku": "SV-RUSH-01",
        "keywords": ["rush", "expedited", "shipping", "fast"]
    },
    "monthly_subscription": {
        "name": "Monthly Supply Subscription",
        "description": "Recurring monthly order with 15% discount + free shipping",
        "category": "subscription",
        "unit": "month",
        "price_per_unit": 0,  # Custom quote
        "min_order": 1,
        "sku": "SUB-MONTHLY",
        "keywords": ["subscription", "recurring", "monthly"]
    },
    "consultation": {
        "name": "Business Supply Consultation",
        "description": "Expert consultation on optimizing your supply chain",
        "category": "service",
        "unit": "hour",
        "price_per_unit": 125.00,
        "min_order": 1,
        "sku": "SV-CONSULT",
        "keywords": ["consultation", "business", "supply chain"]
    },
}

# Categories for organization
CATEGORIES = {
    "thermal_paper": {
        "name": "Thermal Receipt Paper",
        "description": "Premium thermal rolls for POS systems",
        "icon": "🧾"
    },
    "paper": {
        "name": "Bond & Copy Paper",
        "description": "Standard paper for printers and copiers",
        "icon": "📄"
    },
    "ink_toner": {
        "name": "Ink & Toner",
        "description": "Printer ink and toner cartridges",
        "icon": "🖨️"
    },
    "pos_supplies": {
        "name": "POS Supplies",
        "description": "Point of sale equipment and supplies",
        "icon": "💳"
    },
    "labels": {
        "name": "Labels & Tags",
        "description": "Shipping labels, price tags, and product labels",
        "icon": "🏷️"
    },
    "service": {
        "name": "Services",
        "description": "Setup, support, and consulting services",
        "icon": "🔧"
    },
    "discount": {
        "name": "Discounts",
        "description": "Volume and promotional discounts",
        "icon": "💰"
    },
    "subscription": {
        "name": "Subscriptions",
        "description": "Recurring supply programs",
        "icon": "📦"
    }
}

def get_all_products():
    """Return all products as list"""
    return PRODUCTS

def get_all_services():
    """Return all services as list"""
    return SERVICES

def get_products_by_category(category):
    """Get products filtered by category"""
    return {k: v for k, v in PRODUCTS.items() if v.get('category') == category}

def get_product_by_sku(sku):
    """Get product by SKU"""
    for p in PRODUCTS.values():
        if p.get('sku') == sku:
            return p
    for s in SERVICES.values():
        if s.get('sku') == sku:
            return s
    return None

def search_products(query):
    """Search products by keywords"""
    query = query.lower()
    results = {}
    
    for key, product in {**PRODUCTS, **SERVICES}.items():
        keywords = [k.lower() for k in product.get('keywords', [])]
        name = product.get('name', '').lower()
        desc = product.get('description', '').lower()
        
        if query in name or query in desc or query in keywords:
            results[key] = product
    
    return results

def calculate_order(items):
    """Calculate order total with discounts"""
    subtotal = 0
    line_items = []
    
    for item in items:
        product = get_product_by_sku(item.get('sku'))
        if not product:
            continue
        
        qty = item.get('quantity', 1)
        unit_price = product.get('price_per_unit', 0)
        line_total = unit_price * qty
        
        line_items.append({
            'sku': product.get('sku'),
            'name': product.get('name'),
            'quantity': qty,
            'unit_price': unit_price,
            'line_total': line_total,
            'category': product.get('category')
        })
        
        subtotal += line_total
    
    # Apply bulk discount if applicable
    discount = 0
    if subtotal >= 500:
        discount = subtotal * 0.10  # 10% off orders over $500
    
    tax_rate = 0.0825  # California tax rate
    tax = (subtotal - discount) * tax_rate
    total = subtotal - discount + tax
    
    return {
        'items': line_items,
        'subtotal': subtotal,
        'discount': discount,
        'discount_percent': 10 if discount > 0 else 0,
        'tax': tax,
        'tax_rate': tax_rate,
        'total': total
    }

if __name__ == "__main__":
    print("PSDEPOT Product Catalog")
    print("=" * 50)
    print(f"\n{len(PRODUCTS)} Products")
    print(f"{len(SERVICES)} Services")
    print(f"{len(CATEGORIES)} Categories")
    print("\nCategories:")
    for cat, info in CATEGORIES.items():
        print(f"  {info['icon']} {info['name']}")
