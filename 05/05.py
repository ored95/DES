"""
Author: Binh D. Nguyen
Problem: Speed and Distance
"""
import numpy as np

class ANFIS(object):
    def __init__(self, X, Y, targets, n_rules, p, q, r, learning_rate=1e-2):
        # Length of inputs and target must be equal
        self.N = len(targets)
        self.X = X
        self.Y = Y
        self.targets = targets
        self.R = n_rules
        self.learning_rate = learning_rate
        
        self.LA = np.zeros(shape=(3,2))     # 3 x 2
        self.LB = np.zeros(shape=(3,2))     # 3 x 2
        self.LA = [[1, 4], [2, 3], [3, 1]]  # Initial
        self.LB = [[1, 3], [2, 2], [3, 0.5]]

        self.FP = p         # 9
        self.FQ = q         # 9
        self.FR = r         # 9
        self.errors = list()

    # Overall Output function
    def f(self, ia, ib, x, y):
        index = 3 * ia + ib
        return self.FP[index] * x + self.FQ[index] * y + self.FR[index]
    
    # First membership function
    def levelA(self, x, ia):
        return 1.0 / (1.0 + ((x - self.LA[ia][1]) / self.LA[ia][0]) ** 2.0)

    # Derivative of levelA by a
    def dlevelA_0(self, x, ia):
        return 2.0 * self.levelA(x, ia)**2.0 * (x - self.LA[ia][1]) / (self.LA[ia][0] ** 2.0)  

    # Derivative of levelA by c
    def dlevelA_1(self, x, ia):
        return 2.0 * self.levelA(x, ia)**2.0 / self.LA[ia][0]

    # Second membership function
    def levelB(self, y, ib):
        return 1.0 / (1.0 + ((y - self.LB[ib][1]) / self.LB[ib][0]) ** 2.0)

    # Derivative of levelB by a
    def dlevelB_0(self, y, ib):
        return 2.0 * self.levelB(y, ib)**2.0 * (y - self.LB[ib][1]) / (self.LB[ib][0] ** 2.0)  

    # Derivative of levelB by c
    def dlevelB_1(self, y, ib):
        return 2.0 * self.levelB(y, ib)**2.0 / self.LB[ib][0]

    # Learning process
    def train(self, n_epoches=10):
        for epoch in range(n_epoches):
            # Forward pass
            F = np.zeros(self.N)
            U = np.zeros(self.N)
            V = np.zeros(self.N)

            for p in range(self.N):
                for ia in range(len(self.LA)):
                    wpi = self.levelA(x=self.X[p], ia=ia)
                    
                    fba = 0.0
                    wba = 0.0
                    for ib in range(len(self.LB)):
                        w = self.levelB(y=self.Y[p], ib=ib)
                        fba += self.f(ia, ib, self.X[p], self.Y[p]) * w
                        wba += w

                    U[p] += fba * wpi
                    V[p] += wba * wpi
                
                # final wrap
                F[p] += U[p] / V[p]
            
            # Process error
            error = sum([(self.targets[p] - F[p]) ** 2.0 for p in range(self.N)])
            self.errors.append(error)
            
            # Change learning rate (advanced)
            if len(self.errors) > 2:
                if self.errors[-1] > self.errors[-2]:
                    self.learning_rate *= -1
                
                    if self.errors[-2] < self.errors[-3]:
                        self.learning_rate *= 1.05
                    else:
                        self.learning_rate *= 0.95
            
            # Backward pass
            dEA_0 = np.zeros(len(self.LA))      # LA: A
            dEA_1 = np.zeros(len(self.LA))      # LA: C
            dEB_0 = np.zeros(len(self.LB))      # LB: A
            dEB_1 = np.zeros(len(self.LB))      # LB: C

            for p in range(self.N):
                # Part 0 of formula d(error), applying for both A and B
                part0 = -2.0 * (self.targets[p] - F[p])

                part1A = np.zeros(len(self.LA))
                part1B = np.zeros(len(self.LB))                

                # Part 1 of formula d(error), applying for A
                for ia in range(len(self.LA)):
                    dUa = 0.0
                    dVa = 0.0
                    for ib in range(len(self.LB)):
                        w = self.levelB(y=self.Y[p], ib=ib)
                        dUa += self.f(ia, ib, self.X[p], self.Y[p]) * w
                        dVa += w
                    part1A[ia] = dUa / V[p] - dVa * U[p] / (V[p] ** 2.0)
                
                # Part 1 of formula d(error), applying for B 
                for ib in range(len(self.LB)):
                    dUb = 0.0
                    dVb = 0.0
                    for ia in range(len(self.LA)):
                        w = self.levelA(x=self.X[p], ia=ia)
                        dUb += self.f(ia, ib, self.X[p], self.Y[p]) * w
                        dVb += w
                    part1B[ib] = dUb / V[p] - dVb * U[p] / (V[p] ** 2.0)

                # Part 2 of formula d(error), applying for A
                for ia in range(len(self.LA)):
                    part2A_0   = self.dlevelA_0(x=self.X[p], ia=ia)
                    dEA_0[ia] += part0 * part1A[ia] * part2A_0

                    part2A_1   = self.dlevelA_1(x=self.X[p], ia=ia)
                    dEA_1[ia] += part0 * part1A[ia] * part2A_1

                # Part 2 of formula d(error), applying for B
                for ib in range(len(self.LB)):
                    part2B_0   = self.dlevelB_0(y=self.Y[p], ib=ib)
                    dEB_0[ib] += part0 * part1B[ib] * part2B_0

                    part2B_1   = self.dlevelB_1(y=self.Y[p], ib=ib)
                    dEB_1[ib] += part0 * part1B[ib] * part2B_1

            # Now update our coefficients
            for ia in range(len(self.LA)):
                self.LA[ia][0] -= self.learning_rate * dEA_0[ia]
                self.LA[ia][1] -= self.learning_rate * dEA_1[ia]

            for ib in range(len(self.LB)):
                self.LB[ib][0] -= self.learning_rate * dEB_0[ib]
                self.LB[ib][1] -= self.learning_rate * dEB_1[ib]

            # Display errors
            print('Epoch={:3d}\tError={:.5f}'.format(epoch, self.errors[-1]))

    def predict(self, x, y):
        U = 0.0
        V = 0.0
        for ia in range(len(self.LA)):
            wpi = self.levelA(x=x, ia=ia)
            
            fba = 0.0
            wba = 0.0
            for ib in range(len(self.LB)):
                w = self.levelB(y=y, ib=ib)
                fba += self.f(ia, ib, x, y) * w
                wba += w

            U += fba * wpi
            V += wba * wpi
            
        # overall output
        return U / V

if __name__ == "__main__":
    V1 = [20, 60, 100, 24, 70, 110, 15, 50, 90]     # Input 1
    D_ = [ 5,  8,  12, 15, 30,  28, 32, 31, 36]     # Input 2
    V2 = [20, 59, 101, 17, 58,  90,  8, 36, 62]     # Target

    # Output coefficients
    P = [ 1,    1, 1.2,    1,   1.2, 1.1,  3, 1.5,    1]    
    Q = [-1, -1.5,  -3, -0.5, -0.75,  -1, -1,  -1, -0.5]
    R = [ 5, 11.0,  17,  0.5,  -3.5,  -3, -5,  -8,  -10]

    anfis = ANFIS(
        X=V1,
        Y=D_,
        targets=V2,
        n_rules=9,
        p=P,
        q=Q,
        r=R,
        learning_rate=0.5
    )

    import sys
    print("!! Process training starts..\n")
    anfis.train(n_epoches=int(sys.argv[1]))
    print("!! Process training finished.\n")
    
    try:
        while True:
            print("V1: " + str(anfis.predict(   \
                x=float(input("V2: ")),         \
                y=float(input(" D: "))          \
            )) + "\n")
    except ValueError:
        print("Exiting program..")