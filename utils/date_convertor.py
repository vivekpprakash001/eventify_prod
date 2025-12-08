from datetime import datetime

def convert_date_to_dd_mm_yyyy(date_str):
    if isinstance(date_str, datetime.date):
        return date_str.strftime("%d-%m-%Y")
    
    # If the input is a string → parse it as YYYY-MM-DD
    if isinstance(date_str, str):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d-%m-%Y")
        except ValueError:
            raise ValueError("String date must be in 'YYYY-MM-DD' format")
    
    # Unsupported type
    raise TypeError("Input must be a string or datetime.date object")