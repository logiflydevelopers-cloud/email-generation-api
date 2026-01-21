import re
from typing import Tuple, Optional

def extract_dates(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts two dates in DD/MM/YYYY format from text.
    Returns (start_date, end_date) or (None, None).
    """
    pattern = r"(\d{2}/\d{2}/\d{4})"
    matches = re.findall(pattern, text)

    if len(matches) >= 2:
        return matches[0], matches[1]

    return None, None
