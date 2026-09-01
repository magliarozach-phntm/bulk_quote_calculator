def calculate_quote(quantity, unit_cost, shipping_cost, markup):
    shipping_per_unit = shipping_cost / quantity
    landed_cost = unit_cost + shipping_per_unit
    quote_price = landed_cost * (1 + markup / 100)

    return {
        "shipping_per_unit": round(shipping_per_unit, 2),
        "landed_cost": round(landed_cost, 2),
        "quote_price": round(quote_price, 2)
    }
    
if __name__ == '__main__':
    result = calculate_quote(
        quantity=500,
        unit_cost=4.25,
        shipping_cost=350,
        markup=20
    )
    print(result)