# experiment_table.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from brain import NeuralNetwork
from laboratory import plot_decision_boundary, plot_network_structure

# 1. Create a fresh, untrained brain with flexible structure
# [Input, Hidden1, Hidden2, Output]
ai_agent = NeuralNetwork([2, 4, 4, 1])

# Training Data (XOR Problem)
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([[0], [1], [1], [0]])

print("Experiment Started...")
print(
    "A window will open showing the internal structure and the decision map of the AI."
)

# 2. Setup the Visualization Window
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plt.subplots_adjust(bottom=0.2)  # Make room for the button at the bottom


def update_display():
    """
    Clears and redraws the plots with the current state of the network.
    """
    ax1.clear()
    ax2.clear()

    # Left Panel: Structure
    plot_network_structure(ax1, ai_agent)

    # Right Panel: Decision Map
    plot_decision_boundary(ax2, ai_agent)

    plt.draw()


# Draw the initial state
update_display()


# 3. Add Interactivity (Buttons)
class ControlPanel:
    def trigger_mutation(self, event):
        # Apply random changes to the network weights
        ai_agent.mutate(rate=0.5)
        print("Network Mutated! Weights have shifted.")
        update_display()

    def trigger_training(self, event):
        # Run Backpropagation
        print("Training with Backprop (2000 epochs)...")
        # Run a burst of training
        for _ in range(2000):
            ai_agent.forward(X_train)
            ai_agent.backward(X_train, y_train, learning_rate=0.5)

        # Calculate final loss for display
        loss = np.mean(np.square(y_train - ai_agent.activations[-1]))
        print(f"Training Done. Loss: {loss:.5f}")
        update_display()


callback = ControlPanel()

# Place the buttons on the plot
# [left, bottom, width, height]

# Mutate Button
ax_mutate = plt.axes([0.25, 0.05, 0.2, 0.075])
btn_mutate = Button(ax_mutate, "Mutate (Random)\n(Explore)")
btn_mutate.on_clicked(callback.trigger_mutation)

# Train Button
ax_train = plt.axes([0.55, 0.05, 0.2, 0.075])
btn_train = Button(ax_train, "Train (Backprop)\n(Learn)")
btn_train.on_clicked(callback.trigger_training)

plt.show()
