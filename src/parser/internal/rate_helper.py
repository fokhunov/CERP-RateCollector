from decimal import Decimal


# from_string() transforms rate value from string
def from_string(val):
    if isinstance(val, basestring):
        val = val.replace(" ", "").strip()
        if ',' in val and '.' in val:
            # if we have dot '.' and comma ',' -> comma used as thousand separation so ignore it
            val = val.replace(",", "")
        else:
            val = val.replace(",", ".")
    if val == "" or val is None:
        return 0

    val = round(Decimal(val) * 10000)
    return int(val)


# is_empty returns true if bank rates value is empty
def is_empty(bank_rates):
    for field in bank_rates:
        if bank_rates[field] != 0:
            return False

    return True
