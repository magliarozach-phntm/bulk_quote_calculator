from validator import validate_row

TEST_CONFIG = {
    "minimum_markup": 0,
    "maximum_markup": 100
}

def test_is_valid_row():
    errors = validate_row({
        "sku": "ABC123",
        "quantity": 500,
        "unit_cost": 4.25,
        "shipping_cost": 350,
        "markup": 20
    }, TEST_CONFIG)

    assert errors == []

def test_invalid_row_returns_all_errors():
    errors = validate_row({
        "sku": "",
        "quantity": 0,
        "unit_cost": -4.25,
        "shipping_cost": -350,
        "markup": -20
    }, TEST_CONFIG)

    assert len(errors) == 5
    assert "SKU is required." in errors 
    assert "Quantity must be a positive integer." in errors
    assert "Unit cost must be non-negative." in errors
    assert "Shipping cost must be non-negative." in errors
    assert "Markup must be between 0 and 100." in errors


def test_markup_above_config_maximum_is_rejected():
    errors = validate_row({
        'sku': 'ABC123',
        'quantity': 500,
        'unit_cost': 4.25,
        'shipping_cost': 350,
        "markup": 125
    }, TEST_CONFIG)
    
    assert "Markup must be between 0 and 100." in errors