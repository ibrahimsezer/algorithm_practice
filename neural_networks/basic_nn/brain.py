# brain.py
import numpy as np


class NeuralNetwork:
    def __init__(self, input_size=2, hidden_size=4, output_size=1):
        """
        Initializes the Neural Network with random weights.
        Structure: Input Layer -> Hidden Layer 1 -> Hidden Layer 2 -> Output Layer
        """
        self.sizes = [input_size, hidden_size, hidden_size, output_size]

        # Initialize weights (W) and biases (b)
        # Weights determine the strength of the connection between neurons.
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))

        self.W2 = np.random.randn(hidden_size, hidden_size)
        self.b2 = np.zeros((1, hidden_size))

        self.W3 = np.random.randn(hidden_size, output_size)
        self.b3 = np.zeros((1, output_size))

    def sigmoid(self, x):
        """
        Activation function: Squashes numbers into range [0, 1].
        This allows the network to make probability-like decisions.
        """
        return 1 / (1 + np.exp(-x))

    def forward(self, X):
        """
        Forward Pass: Takes input X, passes it through layers, returns prediction.
        """
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

    def mutate(self, rate=0.1):
        """
        Randomly alters the weights of the network.
        This simulates 'evolution' or 'learning' by changing how the network thinks.
        """
        self.W1 += np.random.randn(*self.W1.shape) * rate
        self.W2 += np.random.randn(*self.W2.shape) * rate
        self.W3 += np.random.randn(*self.W3.shape) * rate
