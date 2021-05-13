import math

def my_round(decimals):
    fractional_path = decimals - math.floor(decimals)
    if fractional_path * 100 >= 50:
        return math.ceil(decimals)
    else:
        return math.floor(decimals)