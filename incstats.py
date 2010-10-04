
class IncrementalStats:
    """Basic incremental stats."""
    def __init__(self):
        self.sum = 0
        self.min = 1e30000
        self.max = -1e30000
        self.n = 0

    def add(self, x):
        self.sum += x
        self.n += 1

        if x < self.min:
            self.min = x

        if x > self.max:
            self.max = x

    def avg(self):
        if self.n == 0:
            return self.min / self.max

        return 1.0 * self.sum / self.n

