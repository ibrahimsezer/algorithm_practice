# experiment_table.py
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from brain import NeuralNetwork
from laboratory import plot_decision_boundary, plot_network_structure

# 1. Create a fresh, untrained brain
ai_agent = NeuralNetwork()

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


# 3. Add Interactivity (Button)
class ControlPanel:
    def trigger_mutation(self, event):
        # Apply random changes to the network weights
        ai_agent.mutate(rate=0.5)
        print("Network Mutated! Weights have shifted.")
        update_display()


callback = ControlPanel()

# Place the button on the plot
# [left, bottom, width, height]
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
btn_mutate = Button(ax_button, "Mutate Network\n(Click to Learn/Change)")
btn_mutate.on_clicked(callback.trigger_mutation)

plt.show()
