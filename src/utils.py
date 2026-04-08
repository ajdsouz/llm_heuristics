from time import perf_counter

def timer(func):
    """
    A timer decorator to compute runtime of a function

    Args:
        func (_type_): A function whose runtime needs to be computed
    """
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        return result, (end - start)
    return wrapper