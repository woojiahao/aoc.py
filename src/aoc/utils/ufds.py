from typing import Dict


class UFDS:
    def __init__(self, n: int) -> None:
        self.n = n
        self.parents = list(range(n))
        self.ranks = [1] * n
        self.unions = n

    def find(self, p) -> int:
        if self.parents[p] == p:
            return p
        self.parents[p] = self.find(self.parents[p])
        return self.parents[p]

    def union(self, p, q) -> None:
        root_p, root_q = self.find(p), self.find(q)
        if root_p != root_q:
            self.unions -= 1

        if self.ranks[root_p] < self.ranks[root_q]:
            self.ranks[root_q] += self.ranks[root_p]
            self.parents[root_p] = root_q
        else:
            self.ranks[root_p] += self.ranks[root_q]
            self.parents[root_q] = root_p

    @property
    def union_sizes(self) -> Dict[int, int]:
        sizes: Dict[int, int] = {}
        for p in range(self.n):
            root_p = self.find(p)
            sizes[root_p] = sizes.get(root_p, 0) + 1
        return sizes
