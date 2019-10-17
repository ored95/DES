import numpy as np

NUMBER_POINTS = 1000

class Solution(object):
    def __init__(self, fuzzies, titles, plt, points, sugeno):
        self.fuzzies = fuzzies
        self.titles  = titles
        self.plt     = plt
        self.figure  = plt.figure()
        self.points  = points
        self.sugeno = sugeno

    # Example: colors = ['tab:blue', 'tab:orange', 'tab:red']
    def plot_fuzzy(self, axis, index_fuzzy, colors, n=NUMBER_POINTS):
        # Set range X-axis
        Xmax = 0
        for type_ in self.fuzzies[index_fuzzy].dict_:
            Xmax = max(max([p[0] for p in self.fuzzies[index_fuzzy].dict_[type_]]), Xmax)
        X = np.linspace(0, Xmax * 1.2, n)
        
        # Plot our data
        i = 0
        for type_ in self.fuzzies[index_fuzzy].dict_:
            Y = [self.fuzzies[index_fuzzy].getLevel(x, type_) for x in X]
            axis.plot(X, Y, color=colors[i])
            i += 1

        # Plot max level line: (1)
        axis.plot([0, max(X)], [1, 1], 'r--', color='black', linewidth=0.5)
        
        # Plot cross points
        ispec = 1       # By default: level
        if index_fuzzy == -1:
            ispec = -1  # Center mass
        for p in self.points[self.titles[index_fuzzy]]:
            axis.scatter(p[0], p[ispec], color='tab:green')
            axis.plot([p[0], p[0]], [0, 1.2], 'r--', color='black', linewidth=0.5)      # Vertical cross
            m = p[0]
            if index_fuzzy == -1:
                m = max(X)
            axis.plot([0, m * 1.1], [p[1], p[1]], 'r--', color='black', linewidth=0.5)  # Horizontal cross

            # Texts
            axis.text(p[0]*1.01, p[ispec]*1.01, '({:.2f}, {:.2f})'.format(p[0], p[ispec]))

        # set the limits
        axis.set_xlim([0, max(X)])
        axis.set_ylim([0, 1.2])
        
        # Set titles
        axis.set_title(self.titles[index_fuzzy])

    def plot_fuzzies(self, n=NUMBER_POINTS):
        ax1 = self.figure.add_subplot(2, 2, 1)
        self.plot_fuzzy(ax1, 0, colors=['tab:blue', 'tab:orange', 'tab:red'])
        
        ax2 = self.figure.add_subplot(2, 2, 3)
        self.plot_fuzzy(ax2, 1, colors=['tab:blue', 'tab:orange', 'tab:red'])
        
        ax3 = self.figure.add_subplot(2, 2, 2)
        self.plot_fuzzy(ax3, -1, colors=['tab:blue', 'tab:orange', 'tab:red'])
        
        ax3.scatter(self.sugeno[0], self.sugeno[1], color='tab:pink')
        self.plt.show()