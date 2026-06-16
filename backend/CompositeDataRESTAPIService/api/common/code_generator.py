from random import sample

SEQUENCE = "1234567890asdfghjklqwertyuiopzxcvbnm"


def generate_sequence(k: int = 10) -> str:
    """
    Создание уникальной последовастельности, используя SEQUENCE
    :param k:
    :return: unique sequence
    """

    return "".join(sample(SEQUENCE, k=k))
