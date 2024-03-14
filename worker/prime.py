import math


def is_prime(number):
    if number % 6 not in [1, 5]:
        return False

    for i in range(5, math.isqrt(number) + 1, 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True
