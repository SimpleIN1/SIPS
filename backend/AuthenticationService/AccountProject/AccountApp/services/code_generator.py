import itertools
import random

sequence = list(itertools.product("1234567890", repeat=6))


def generate_code():
    i = random.randint(0, 999999)
    return "".join(sequence[i])
