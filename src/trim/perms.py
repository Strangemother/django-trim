from collections import defaultdict


class SlofTuple(tuple):
    """A tuple class with the additional `slice of` method or `slof(i)`
    returning `x[n] of x in self`.

        content += (('c', 'b'), ('g', 'r'),)
        content.slof(0)
        ('c', 'g',)

    """

    def slof(self, index):
        return self.__class__(x[index] for x in self)


class EasyPermissionString(object):

    def __init__(self, strs=None, index=0, positions=None):
        self.index = index
        self.positions = positions or defaultdict(set)
        self.strs = strs or SlofTuple()

    def __getattr__(self, k):
        return self.push(self.index, k)

    def push(self, index, *items):
        # strs = self.strs + tuple((index, x,) for x in items)
        copy = self.__class__(self.strs, index, self.positions)
        copy.positions[index].update(items)
        print("Copied", copy.positions)
        return copy

    @property
    def crud(self):
        return self.push(
            2,
            "add",
            "view",
            "change",
            "delete",
        )

    def __add__(self, other):
        if isinstance(other, str):
            return self.push(self.index, other)
        if isinstance(other, (tuple, list)):
            return self.push(self.index, *other)

        raise Exception("Cannot add type", type(other))
        return self

    def as_tuple(self):
        # Iterate the strs, split on positions in each,
        count = 2
        if len(self.positions) > 0:
            count = max(self.positions.keys()) + 1
        print("count", count)
        for i in range(count):
            try:
                self.positions[i].add(self.strs[i][1])
            except IndexError:
                pass
            # for index, key in self.strs:
            pos = self.positions[i].copy()
            print(" ", pos)

    def flat(self):
        return ".".join([x[1] for x in self.strs])

    def __str__(self):
        return self.flat()


props = EasyPermissionString()


def test():
    perms = props
    v = perms.stocks.StockCount.crud
    v.as_tuple()

    # assert v == ('stocks.add_stockcount',)


if __name__ == "__main__":
    test()
