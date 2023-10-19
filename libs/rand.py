class Rand:

    def __init__(self, seed: int):
        self.seed = abs(seed) + 131

    def clone(self):
        r = Rand(0)
        r.seed = self.seed
        return r

    def random(self, n):
        return self.int() % n

    def range(self, min_val: float, max_val: float, rand_sign=False):
        return (min_val + self.rand_() * (max_val - min_val)) * (1 if not rand_sign else self.random(2) * 2 - 1)

    def irange(self, min_val: int, max_val: int, rand_sign=False):
        return (min_val + self.random(max_val - min_val + 1)) * (1 if not rand_sign else self.random(2) * 2 - 1)

    def get_seed(self):
        return int(self.seed) - 131

    def rand_(self):
        return (self.int() % 10007) / 10007.0

    def sign(self):
        return self.random(2) * 2 - 1

    def add_seed(self, d: int):
        self.seed = int((self.seed + d) % 2147483647) & 0x3FFFFFFF
        if self.seed == 0:
            self.seed = d + 1

    def init_seed(self, n: int, k=5):
        for _ in range(k):
            n ^= (n << 7) & 0x2b5b2500
            n ^= (n << 15) & 0x1b8b0000
            n ^= n >> 16
            n &= 0x3FFFFFFF
            h = 5381
            h = (h << 5) + h + (n & 0xFF)
            h = (h << 5) + h + ((n >> 8) & 0xFF)
            h = (h << 5) + h + ((n >> 16) & 0xFF)
            h = (h << 5) + h + (n >> 24)
            n = h & 0x3FFFFFFF

        self.seed = (n & 0x1FFFFFFF) + 131

    def int(self):
        self.seed = (self.seed * 16807) % 2147483647
        return self.seed & 0x3FFFFFFF