from functools import wraps

def validate_parameters(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None or (isinstance(arg, str) and not arg):
                raise ValueError("None or empty string parameter found")
        for key, value in kwargs.items():
            if value is None or (isinstance(value, str) and not value):
                raise ValueError("None or empty string parameter found")
        return func(*args, **kwargs)
    return wrapper