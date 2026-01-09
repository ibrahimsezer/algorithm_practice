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
    # cmap="RdBu" creates a Red-White-Blue gradient.
    # vmin=0, vmax=1 ensures the colors are pinned to [0, 1] range.
    ax.contourf(X, Y, Z, cmap="RdBu", alpha=0.8, levels=20, vmin=0, vmax=1)

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

    # Dynamic spacing calculations
    # Ensure vertical spacing is tight enough if there are many neurons
    max_neurons = max(layer_sizes)
    v_spacing = 1.0 / (max_neurons + 1)
    h_spacing = 1.0 / (len(layer_sizes) + 0.1)

    # Scale neuron size based on density
    # If many neurons, make circles smaller
    circle_radius = min(v_spacing / 3.0, 0.04)

    # Draw Neurons (Circles)
    for n, layer_size in enumerate(layer_sizes):
        # layer_top = 0.5 + (layer_size - 1) * v_spacing / 2.0
        # Wait, typical centering:
        # If height is 1.0. Layer spans (layer_size-1)*v_spacing.
        # Center is 0.5. Top is 0.5 + span/2.

        # Proper centering calculation:
        layer_height = (layer_size - 1) * v_spacing
        start_y = 0.5 + layer_height / 2.0

        for m in range(layer_size):
            x = (n + 0.5) * h_spacing
            y = start_y - m * v_spacing

            # White circle with black edge
            circle = plt.Circle((x, y), circle_radius, color="w", ec="k", zorder=4)
            ax.add_artist(circle)

            # Add labels for Input and Output layers
            if n == 0:
                ax.text(
                    x, y - circle_radius * 2, f"In {m + 1}", ha="center", fontsize=8
                )
            elif n == len(layer_sizes) - 1:
                ax.text(x, y - circle_radius * 2, "Out", ha="center", fontsize=8)

            # Store positions for line drawing (not needed if we loop again or cache)
            # Actually, we need to loop again for lines.
            # To simplify, we can just recalculate coordinates (cheap).

    # Draw Connections (Synapses/Weights)
    # We draw faint lines to represent the dense connectivity
    for n, (layer_size_a, layer_size_b) in enumerate(
        zip(layer_sizes[:-1], layer_sizes[1:])
    ):
        layer_height_a = (layer_size_a - 1) * v_spacing
        start_y_a = 0.5 + layer_height_a / 2.0

        layer_height_b = (layer_size_b - 1) * v_spacing
        start_y_b = 0.5 + layer_height_b / 2.0

        for m in range(layer_size_a):
            for o in range(layer_size_b):
                x_a = (n + 0.5) * h_spacing
                y_a = start_y_a - m * v_spacing

                x_b = ((n + 1) + 0.5) * h_spacing
                y_b = start_y_b - o * v_spacing

                line = plt.Line2D(
                    [x_a + circle_radius, x_b - circle_radius],
                    [y_a, y_b],
                    c="gray",
                    alpha=0.3,
                )
                ax.add_artist(line)

    ax.axis("off")
    ax.set_title("Network Anatomy")
