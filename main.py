from excel_io import read_quotes, write_results
from calculator import calculate_quote
from validator import validate_row
from config_loader import load_config


def process_quotes(input_filename, output_filename):
    quotes = read_quotes(input_filename)
    
    results = []
    error_rows = []
    
    config = load_config()
    
    for quote in quotes:
        errors = validate_row(quote, config)
        
        if errors:
            error_rows.append({
                'sku': quote['sku'],
                'errors': errors
            })
            continue
        
        calculation = calculate_quote(
            quantity=quote['quantity'],
            unit_cost=quote['unit_cost'],
            shipping_cost=quote['shipping_cost'],
            markup=quote['markup']
        )
        
        results.append({
            **quote,
            **calculation
        })
        
    write_results(
        output_filename,
        results,
        error_rows
    )
    
    return {
        'successful': len(results),
        'errors': len(error_rows)
    }
    
if __name__ == '__main__':
    config = load_config()
    summary = process_quotes(
        'sample_input.xlsx',
        config['output_filename']
    )
    
    print(summary)