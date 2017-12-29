from decimal import Decimal


# possibly incomplete; may need to convert other types
def simplify_type_for_gizeh(val):
    if type(val) is Decimal:
        return float(val)
    elif type(val) in (list, tuple):
        return map(simplify_type_for_gizeh, val)
    else:
        return val
