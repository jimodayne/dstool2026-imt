import datetime

def parse_iso_date(date_string: str) -> datetime:
    """Parse an ISO 8601 date string and return a datetime object.
    Raise ValueError with a clear message if the format is invalid."""
    
    