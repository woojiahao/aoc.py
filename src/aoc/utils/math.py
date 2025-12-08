from typing import Tuple


def sign(num: int) -> int:
    if num == 0:
        return 0
    elif num < 0:
        return -1
    else:
        return 1


def euclidean_distance(a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
    ans = 0
    for p, q in zip(a, b):
        ans += (p - q) ** 2
    return ans**0.5
