
MAX_ITERATIONS = 1000

class Fuzzy(object):
    # Example: {"LOW": [[5, 0], [15, 1], [20, 0.4], [30, 0]], "MED": [], ..]}
    def __init__(self, dict_):
        self.dict_ = dict_
        
    def bSearch(self, value, array):
        first = 0
        last = len(array) - 1
        
        if value <= array[first] or value >= array[last]:
            return -1
        
        while (first <= last):
            middle = (first + last) // 2
            if value < array[middle]:
                last = middle - 1
            else:
                first = middle + 1
        return first - 1

    def getLevel(self, x, type_):
        i = self.bSearch(x, [d[0] for d in self.dict_[type_]])
        if i == -1:
            return 0
        else:
            p1 = self.dict_[type_][i]
            p2 = self.dict_[type_][i + 1]

            if p1[1] == p2[1]:
                return p1[1]
            else:
                return p1[1] + (x - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0])

    def __quick_2p(self, x, segment):
        if segment[0][1] == segment[1][1]:
            return segment[0][1]
        else:
            return segment[0][1] + (x - segment[0][0]) * (segment[1][1] - segment[0][1]) / (segment[1][0] - segment[0][0])

    def level_by_X(self, value):
        r = dict()
        for type_ in self.dict_:
            level =  self.getLevel(value, type_)
            if level:
                r[type_] = level
        return r

    # Calculate level by given segment
    def level_help(self, x, level_, segment):
        return min(self.__quick_2p(x, segment), level_)

    '''
    Apply Sympson's rule to define integral
    '''
    def СenterOfGravity(self, type_, level_, n=MAX_ITERATIONS):
        # Fix Sympson's rule condition
        if n % 2 != 0:
            n *= 2

        # Get our configuration
        Area = [x for x in self.dict_[type_]]

        # Initialize out stuff
        step = (Area[-1][0] - Area[0][0]) / n
        i = 0
        x = Area[i][0] + step

        S = min(level_, Area[0][1]) + min(level_, Area[-1][1])
        Lx = Area[i][0] * min(level_, Area[0][1]) + Area[-1][0] * min(level_, Area[-1][1])
        Ly = min(level_, Area[0][1]) ** 2 + min(level_, Area[0][1]) ** 2

        for _ in range(1, n // 2):
            if x >= Area[i][0] and x < Area[i+1][0]:
                y1 = self.level_help(       x, level_, [Area[i], Area[i+1]])
                y2 = self.level_help(x + step, level_, [Area[i], Area[i+1]])
                S  += 4.0 * y1 + 2.0 * y2
                Lx +=  x * y1 + (x + step) * y2
                Ly += y1 * y1 + y2 * y2
                x += 2.0 * step
            else:
                i += 1
        
        S  *= step / 3.0
        Lx *= step
        Ly *= step / 2.0

        return Lx / S, Ly / S