def clean_value(value):
    if value is None or value == "":
        return "—"
    return value