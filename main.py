def main():
    print("Hello from dstool2026-imt!")


if __name__ == "__main__":
    main()


import datetime

def parse_iso_date(date_string: str) -> datetime:
    """Parse an ISO 8601 date string and return a datetime object.
    Raise ValueError with a clear message if the format is invalid."""
    
    