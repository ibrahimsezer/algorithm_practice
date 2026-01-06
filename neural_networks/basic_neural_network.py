import numpy as np


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
