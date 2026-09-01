def validate_row(row, config):
    errors = []

    if not row["sku"]:
        errors.append("SKU is required.")

    if not is_positive_integer(row["quantity"]):
        errors.append("Quantity must be a positive integer.")

    if not isinstance(row["unit_cost"], (int, float)) or isinstance(row["unit_cost"], bool):
        errors.append("Unit cost must be a number.")
    elif row["unit_cost"] < 0:
        errors.append("Unit cost must be non-negative.")

    if not isinstance(row["shipping_cost"], (int, float)) or isinstance(row["shipping_cost"], bool):
        errors.append("Shipping cost must be a number.")
    elif row["shipping_cost"] < 0:
        errors.append("Shipping cost must be non-negative.")

    if not isinstance(row["markup"], (int, float)) or isinstance(row["markup"], bool):
        errors.append("Markup must be a number.")
    elif not config["minimum_markup"] <= row["markup"] <= config["maximum_markup"]:
        errors.append(
            f"Markup must be between "
            f"{config['minimum_markup']} and "
            f"{config['maximum_markup']}."
        )

    return errors

def is_positive_integer(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value > 0
        and float(value).is_integer()
    )

if __name__ == '__main__':
    row = {
        "sku": "ABC123",
        "quantity": 10,
        "unit_cost": 5.0,
        "shipping_cost": 2.0,
        "markup": 20
    }
    errors = validate_row(row)
    if errors:
        print("Row validation errors:", errors)
    else:
        print("Row is valid.")