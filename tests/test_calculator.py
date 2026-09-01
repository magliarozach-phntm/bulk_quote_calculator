from calculator import calculate_quote

def test_calculate_quote():
    result = calculate_quote(
        quantity=500,
        unit_cost=4.25,
        shipping_cost=350,
        markup=20
    )
    assert result["shipping_per_unit"] == 0.7
    assert result["landed_cost"] == 4.95
    assert result["quote_price"] == 5.94