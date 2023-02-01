def recursive_copy(obj):
    if isinstance(obj, dict):
        return {k: recursive_copy(v) for k, v in obj.items()}
    elif isinstance(obj, set):
        return {recursive_copy(x) for x in obj}
    else:
        return obj