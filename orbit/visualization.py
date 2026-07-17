import matplotlib.pyplot as plt


def plot_orbit(solution):

    x = solution.y[0]
    y = solution.y[1]
    z = solution.y[2]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()