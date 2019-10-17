import csv

class Zadeh(object):
    def __init__(self, fuzzies, csvFileName):
        self.fuzzies = fuzzies
        csv_ = csv.DictReader(open(csvFileName))
        self.rules  = list(csv_)
        self.fields = csv_.fieldnames

    '''
    ### Zadeh operators ###
        AND(x, y) >>    MIN(x, y)
        OR (x, y) >>    MAX(x, y)
        NOT(x)    >>    1 - x
    '''
    def Zadeh(self, X, logic_type='AND'):
        if logic_type == 'AND':
            return min(X)  # x1 * x2
        elif logic_type == 'OR':
            return max(X)  # x1 + x2 - x1 * x2
        elif logic_type == 'NOT':
            return 1 - X[0]
        else:
            return X[0]

    def disp(self):
        for rule in self.rules:
            print(rule)

    # Apply operators for 2 fuzzies and logic_type is AND
    def apply(self, X):
        if len(X) == len(self.fuzzies):
            levels = [self.fuzzies[i].level_by_X(X[i]) for i in range(len(self.fuzzies))] 
            fields = self.fields[:-1]
            
            App = []
            index = 0
            for rule in self.rules:
                # Define which rules shoud be applied
                satisfied = sum(1 for i in range(len(fields)) if rule[fields[i]] in levels[i]) == len(fields)
                if satisfied:
                    App.append([
                        index,
                        rule[self.fields[-1]],
                        self.Zadeh([levels[i][rule[fields[i]]] for i in range(len(fields))])
                    ])

                index += 1

            return App
        else:
            return 'Error: Bad given parameters to apply Zadeh operators!'