from Fuzzy import *
        
Vehicle_2 = Fuzzy({
    "LOW": [ [5, 0], [15, 1], [20, 0.2], [25, 0]],
    "MED": [[20, 0], [24, 0.8], [30, 1], [45, 1], [60, 0]],
    "HIG": [[50, 0], [70, 1], [100, 1], [120, 0]]
})

Vehicle_1 = Fuzzy({
    "LOW": [ [4, 0], [16, 1], [20, 0.32], [24, 0]],
    "MED": [[25, 0], [29, 0.75], [35, 1], [42, 1], [60, 0]],
    "HIG": [[60, 0], [70, 1], [80, 1], [91, 0.7], [108, 0.5], [115, 0]]
})

Distance = Fuzzy({
    "SHOR": [[ 5, 0], [10, 1], [12, 1], [30, 0]],
    "MEDI": [[20, 0], [24, 1], [29, 1], [30, 0]],
    "LONG": [[20, 0], [36, 1], [45, 1], [50, 0]]
})

if __name__ == "__main__":
    try:
        import sys
        from Zadeh import *
        
        fuzzies = [Vehicle_2, Distance, Vehicle_1]
        Z = Zadeh(fuzzies[:-1], sys.argv[1])
        
        data = [
            float(input("Current speed of Vehicle 2: ")),
            float(input("_____Distance between them: "))
        ]

        points = dict()
        for i in range(len(data)):
            Y = fuzzies[i].level_by_X(data[i])
            points[Z.fields[i]] = [[data[i], Y[type_]] for type_ in Y]

        points[Z.fields[-1]] = []
        print("Guess speed of Vehicle 1: ")
        for index, type_, level_ in Z.apply(data):
            x, y = fuzzies[-1].СenterOfGravity(type_, level_)
            points[Z.fields[-1]].append([x, level_, y])
            print("\tR" + str(index + 1) + ". " + type_ + " : " + str(x))

        # Path for Sugeno
        sugeno = list()
        for index, type_, level_ in Z.apply(data):
            x, _ = fuzzies[-1].СenterOfGravity(type_, level_)
            sugeno.append([x, level_])

        SX = sum([x[0] * x[1] for x in sugeno])
        SY = sum([x[1] for x in sugeno])
        print("Sugeno: " + str(SX / SY));
        
        from Solution import *
        import matplotlib.pyplot as plt
        
        s = Solution(
            fuzzies=[Vehicle_2, Distance, Vehicle_1], 
            titles=Z.fields, 
            points=points,
            plt=plt,
            sugeno = [SX / SY, 0]
        )

        s.plot_fuzzies()

    except IndexError:
        print('Command line: python <source> <fileName>')