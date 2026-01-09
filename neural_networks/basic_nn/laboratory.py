# laboratory.py
import numpy as np
import matplotlib.pyplot as plt


def plot_decision_boundary(ax, network):
    """
    Visualizes how the network sees the world.
    - Blue areas: Network predicts close to 0
    - Red areas: Network predicts close to 1
    """
    # Create a 100x100 grid covering the input space (0 to 1)
    x = np.linspace(-0.1, 1.1, 100)
    y = np.linspace(-0.1, 1.1, 100)
    X, Y = np.meshgrid(x, y)

    # Ask the network for a prediction at every single point on the grid
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            input_data = np.array([[X[i, j], Y[i, j]]])
            Z[i, j] = network.forward(input_data)[0, 0]

    # Draw the contour map
    # cmap="RdYlBu" creates a Red-Yellow-Blue gradient
    contour = ax.contourf(X, Y, Z, cmap="RdYlBu", alpha=0.8, levels=20)

    # Plot the specific XOR problem targets (The "Truth")
    # (0,0) and (1,1) should be 0 (Red)
    # (0,1) and (1,0) should be 1 (Blue)
    ax.scatter(
        [0, 1], [0, 1], c="darkred", s=100, edgecolors="white", label="Target: 0 (Red)"
    )
    ax.scatter(
        [0, 1],
        [1, 0],
        c="darkblue",
        s=100,
        edgecolors="white",
        label="Target: 1 (Blue)",
    )

    ax.set_title("Decision Boundary (World View)")
    ax.set_xlabel("Input 1")
    ax.set_ylabel("Input 2")
    ax.legend(loc="upper right", fontsize="small")


def plot_network_structure(ax, network):
    """
    Draws the anatomy of the neural network (Neurons and Connections).
    """
    layer_sizes = network.sizes
    v_spacing = 1.0 / float(max(layer_sizes))
    h_spacing = 1.0 / float(len(layer_sizes) - 1)

    # Draw Neurons (Circles)
    for n, layer_size in enumerate(layer_sizes):
        layer_top = v_spacing * (layer_size - 1) / 2.0 + 0.5
        for m in range(layer_size):
            x = n * h_spacing
            y = layer_top - m * v_spacing

            # White circle with black edge
            circle = plt.Circle((x, y), v_spacing / 4.0, color="w", ec="k", zorder=4)
            ax.add_artist(circle)

            # Add labels for Input and Output layers
            if n == 0:
                ax.text(x, y - 0.1, f"In {m + 1}", ha="center", fontsize=9)
            elif n == len(layer_sizes) - 1:
                ax.text(x, y - 0.1, f"Out", ha="center", fontsize=9)

    # Draw Connections (Synapses/Weights)
    # We draw faint lines to represent the dense connectivity
    for n, (layer_size_a, layer_size_b) in enumerate(
        zip(layer_sizes[:-1], layer_sizes[1:])
    ):
        layer_top_a = v_spacing * (layer_size_a - 1) / 2.0 + 0.5
        layer_top_b = v_spacing * (layer_size_b - 1) / 2.0 + 0.5
        for m in range(layer_size_a):
            for o in range(layer_size_b):
                line = plt.Line2D(
                    [n * h_spacing, (n + 1) * h_spacing],
                    [layer_top_a - m * v_spacing, layer_top_b - o * v_spacing],
                    c="gray",
                    alpha=0.3,
                )
                ax.add_artist(line)

    ax.axis("off")
    ax.set_title("Network Anatomy")
