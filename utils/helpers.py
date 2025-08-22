# import ast

# def extract_linkedin_id(url: str) -> str:
#     """https://www.linkedin.com/in/sonupatel-a-l -> sonupatel-a-l"""
#     return url.rstrip("/").split("/")[-1]

# def safe_parse_jsonish(value):
#     """
#     StaffSpy sometimes returns Python-literal-strings for lists/dicts.
#     Try to parse; if it fails, return the original or a sensible default.
#     """
#     if value is None:
#         return None
#     if isinstance(value, (list, dict)):
#         return value
#     s = str(value).strip()
#     if not s:
#         return None
#     if s.startswith(("[", "{")) and s.endswith(("]", "}")):
#         try:
#             return ast.literal_eval(s)
#         except Exception:
#             return s  # keep raw if unparseable
#     return value

# def coalesce(*vals):
#     for v in vals:
#         if v is not None and str(v).strip() != "":
#             return v
#     return None


import ast


def extract_linkedin_id(url: str) -> str:
    """
    Extracts the LinkedIn profile ID from a full LinkedIn URL.

    Example:
        "https://www.linkedin.com/in/sonupatel-a-l/" -> "sonupatel-a-l"

    Args:
        url (str): Full LinkedIn profile URL

    Returns:
        str: Extracted LinkedIn ID
    """
    return url.rstrip("/").split("/")[-1]


def safe_parse_jsonish(value):
    """
    Tries to safely parse strings that look like Python lists or dicts.

    StaffSpy sometimes returns strings that look like Python literals
    (e.g., "[{'name': 'Python'}, {'name': 'SQL'}]") instead of valid JSON.

    This function uses `ast.literal_eval` to parse it safely.
    If parsing fails, it returns the original string or a sensible fallback.

    Args:
        value: A string, list, dict, or None

    Returns:
        Parsed list/dict if possible, otherwise the original value
    """
    if value is None:
        return None

    if isinstance(value, (list, dict)):
        return value

    s = str(value).strip()
    if not s:
        return None

    # Looks like a list or dict? Try to parse it
    if s.startswith(("[", "{")) and s.endswith(("]", "}")):
        try:
            return ast.literal_eval(s)
        except Exception:
            return s  # Return raw string if parsing fails

    return value


def coalesce(*vals):
    """
    Returns the first non-empty, non-null value from the arguments.

    Useful when trying multiple fallback values (e.g., headline, position, etc.)

    Args:
        *vals: Any number of values

    Returns:
        The first non-empty value, or None
    """
    for v in vals:
        if v is not None and str(v).strip() != "":
            return v
    return None
