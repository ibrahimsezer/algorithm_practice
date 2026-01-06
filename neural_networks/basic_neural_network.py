import numpy as np
import matplotlib.pyplot as plt


class NeuralNetwork:
    def __init__(self, input_size=2, hidden_size=4, output_size=1):
        # Initialize weights and biases for 2 hidden layers
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, hidden_size)
        self.b2 = np.zeros((1, hidden_size))
        self.W3 = np.random.randn(hidden_size, output_size)
        self.b3 = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, X):
        # Layer 1
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        # Layer 2
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        # Output Layer
        self.z3 = np.dot(self.a2, self.W3) + self.b3
        self.output = self.sigmoid(self.z3)
        return self.output


nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)

X_test = np.array([[0, 1]])

predict = nn.forward(X_test)

print(f"Input : {X_test}")
print(f"NN Prediction 0-1: {predict}")


true_value = 1

predict = nn.forward(np.array([[0, 1]]))

error = (true_value - predict) ** 2

print(f"Target: {true_value}, Prediction: {predict[0][0]:.4f}, Error: {error}")
print(f"Error Squared: {error[0][0]:.4f}")

print("Old Prediction:", nn.forward(np.array([[1, 1]])))

nn.W1 = np.ones((2, 4)) * 5
nn.b1 = np.zeros((1, 4))

print("New Prediction:", nn.forward(np.array([[1, 1]])))


def plot_decision_map(network):
    # Create a 100x100 grid between 0 and 1
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)

    # Query the network for each point
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            input_data = np.array([[X[i, j], Y[i, j]]])
            Z[i, j] = network.forward(input_data)[0, 0]

    # Plot the result
    plt.contourf(X, Y, Z, cmap="viridis", levels=20)
    plt.colorbar(label="Network Output (Probability)")
    plt.title("Network Decision Map (Random Weights)")
    plt.xlabel("Input 1")
    plt.ylabel("Input 2")
    plt.show()


# Call the function
plot_decision_map(nn)


# ---

inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

outputs = nn.forward(inputs)
print("Inputs:\n", inputs)
print("Outputs:\n", outputs)
