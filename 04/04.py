"""
========================
Fuzzy c-means clustering
========================
"""
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import sys
"""
----------------------------
1. Data generation and setup
----------------------------
"""
# Define stopping criterion
FERROR = 0.005

# Define colors in plot
colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen', 'deeppink', 'tan', 'slategray']

# Define display-all flag
DISP_ALL = len(sys.argv) > 1

# Define cluster centers
centers = [[4, 2],
           [1, 7],
           [5, 6],
        #    [3, 5]
]

# Define cluster sigmas in x and y, respectively
sigmas = [[0.8, 0.3],
          [0.3, 0.5],
          [1.1, 0.7],
        #   [0.4, 0.9]
]

# Generate test data
np.random.seed(42)  # Set seed for reproducibility
xpts = np.zeros(1)
ypts = np.zeros(1)
labels = np.zeros(1)

# Define total generated points for each class
NPts = 300

# Generating process by normal 
for i, ((xmu, ymu), (xsigma, ysigma)) in enumerate(zip(centers, sigmas)):
    xpts = np.hstack((
                xpts,
                np.random.standard_normal(NPts) * xsigma + xmu
    ))
    ypts = np.hstack((
        ypts,
        np.random.standard_normal(NPts) * ysigma + ymu
    ))
    labels = np.hstack((
        labels,
        np.ones(NPts) * i
    ))

# Visualize the test data
ncenters = i + 1
fig0, ax0 = plt.subplots()
for label in range(ncenters):
    ax0.plot(xpts[labels == label], ypts[labels == label], '.', color=colors[label])
ax0.set_title('Test data: {:d} points x {:d} clusters'.format(NPts, len(centers)))

# Display our data
if not DISP_ALL:
    plt.show()

"""
----------------------------
      2. Clustering
----------------------------
Try to cluster our data by given number of centers
"""
# Set up number of subplots
nr = 4
nc = 3

# Set up the loop and plot
fig1, axes1 = plt.subplots(nc, nr, figsize=(8, 8))
alldata = np.vstack((xpts, ypts))
fpcs = []

for ncenters, ax in enumerate(axes1.reshape(-1), 2):
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        alldata, ncenters, 2, error=FERROR, maxiter=1000, init=None
    )
    
    # Store fpc values for later
    fpcs.append(fpc)

    # Plot assigned clusters, for each data point in training set
    cluster_membership = np.argmax(u, axis=0)
    for j in range(ncenters):
        ax.plot(xpts[cluster_membership == j], 
                ypts[cluster_membership == j], '.', color=colors[j])

    # Mark the center of each fuzzy cluster
    for pt in cntr:
        ax.plot(pt[0], pt[1], 'rs')

    ax.set_title('Centers={0:d}, fpc={1:.2f}'.format(ncenters, fpc))
    ax.axis('off')

fig1.tight_layout()

# Display
if not DISP_ALL:
    plt.show()

"""
----------------------------
    3. Define best fpc
----------------------------
The FPC is defined on the range from 0 to 1. It is a metric which
tells us how cleanly our data is described by a certain model. 
When the FPC is maximized, our data is described best.
"""
i, = np.where(fpcs == max(fpcs))    # Find index of max fpc
ncenters = i[0] + 2                 # Redifine number of centers

fig2, ax2 = plt.subplots()
ax2.plot(np.r_[2:len(fpcs)+2], fpcs)
ax2.set_xlabel("Number of centers")
ax2.set_ylabel("Fuzzy partition coefficient")

# Display
if not DISP_ALL:
    plt.show()

"""
----------------------------
  4. Classifying New Data
----------------------------
We know our best model with which number of cluster centers. 
We'll rebuild a cluster model for use in prediction, generate 
new uniform data, and predict which cluster to which each new 
data point belongs.
"""

# Regenerate fuzzy model with given cluster centers 
# - note that center ordering is random in this clustering algorithm, 
# - so the centers may change places
cntr, u_orig, _, _, _, _, _ = fuzz.cluster.cmeans(
    alldata, ncenters, 2, error=FERROR, maxiter=1000
)

# Show n-cluster model
fig2, ax2 = plt.subplots()
ax2.set_title('Trained model')
for j in range(ncenters):
    ax2.plot(alldata[0, u_orig.argmax(axis=0) == j],
             alldata[1, u_orig.argmax(axis=0) == j], 'o',
             label='series ' + str(j))
ax2.legend()

# Mark the center of each fuzzy cluster
for pt in cntr:
    ax2.plot(pt[0], pt[1], 'rs')

# Display
if not DISP_ALL:
    plt.show()

"""
----------------------------
      5. Prediction
----------------------------
Finally, classify new data via cmeans_predict, incorporating it into the pre-existing model.
"""

# Generate uniformly sampled data spread across the range [0, 10] in x and y
newdata = np.random.uniform(0, 1, (1100, 2)) * 10

# Predict new cluster membership with cntr from the clustered model
u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(
    newdata.T, cntr, 2, error=FERROR, maxiter=1000)

# Plot the classified uniform data
cluster_membership = np.argmax(u, axis=0)  # Hardening for visualization

fig3, ax3 = plt.subplots()
ax3.set_title('Random points classifed according to known centers')
for j in range(ncenters):
    ax3.plot(newdata[cluster_membership == j, 0],
             newdata[cluster_membership == j, 1], 'o',
             label='series ' + str(j))
ax3.legend()

# Mark the center of each fuzzy cluster
for pt in cntr:
    print(pt)
    ax3.plot(pt[0], pt[1], 'rs')

plt.show()