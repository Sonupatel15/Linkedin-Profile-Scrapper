# def extract_linkedin_id(url: str) -> str:
#     """
#     Convert LinkedIn profile URL into ID
#     Example: https://www.linkedin.com/in/sonupatel-a-l -> sonupatel-a-l
#     """
#     return url.rstrip("/").split("/")[-1]


###################


import ast

def extract_linkedin_id(url: str) -> str:
    """https://www.linkedin.com/in/sonupatel-a-l -> sonupatel-a-l"""
    return url.rstrip("/").split("/")[-1]

def safe_parse_jsonish(value):
    """
    StaffSpy sometimes returns Python-literal-strings for lists/dicts.
    Try to parse; if it fails, return the original or a sensible default.
    """
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return value
    s = str(value).strip()
    if not s:
        return None
    if s.startswith(("[", "{")) and s.endswith(("]", "}")):
        try:
            return ast.literal_eval(s)
        except Exception:
            return s  # keep raw if unparseable
    return value

def coalesce(*vals):
    for v in vals:
        if v is not None and str(v).strip() != "":
            return v
    return None
