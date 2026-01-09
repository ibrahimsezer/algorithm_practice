# brain.py
import numpy as np


class NeuralNetwork:
    def __init__(self, layer_sizes=[2, 4, 4, 1]):
        """
        Initializes the Neural Network with random weights and supports dynamic layers.
        :param layer_sizes: List of integers defining the number of neurons in each layer.
        """
        self.sizes = layer_sizes
        self.weights = []
        self.biases = []

        # Initialize weights and biases for each connection between layers
        for i in range(len(layer_sizes) - 1):
            # Weights: (Input_Neurons, Output_Neurons)
            w = np.random.randn(layer_sizes[i], layer_sizes[i + 1])
            # Biases: (1, Output_Neurons)
            b = np.zeros((1, layer_sizes[i + 1]))
            self.weights.append(w)
            self.biases.append(b)

    def sigmoid(self, x):
        """Activation function: Squashes numbers into range [0, 1]."""
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        """Derivative of sigmoid function for backpropagation."""
        s = self.sigmoid(x)
        return s * (1 - s)

    def forward(self, X):
        """
        Forward Pass: Passes input X through the network.
        Stores activations for backpropagation.
        """
        self.activations = [X]  # Store activations layer by layer
        self.z_values = []  # Store linear combinations (z) layer by layer

        input_data = X
        for w, b in zip(self.weights, self.biases):
            z = np.dot(input_data, w) + b
            self.z_values.append(z)
            input_data = self.sigmoid(z)
            self.activations.append(input_data)

        return input_data

    def backward(self, X, y, learning_rate=0.1):
        """
        Backpropagation: Updates weights and biases based on Error (MSE).
        :param X: Input data
        :param y: Target data
        :param learning_rate: Step size for gradient descent
        """
        # 1. Forward pass (ensure we have latest activations)
        # (This usually happens before calling backward, but calling it here ensures state is fresh if needed,
        # though typically we assume forward was just called. For safety in this simple implementation, rely on stored activation)
        # Note: We rely on self.activations from the last forward pass matched with X.
        # Ideally, forward(X) should be called right before this.

        output = self.activations[-1]

        # Calculate Error Gradient at Output Layer
        # Error = Pred - Target
        # Delta = Error * Derivative of Activation
        error = output - y
        delta = error * self.sigmoid_derivative(self.z_values[-1])

        # Gradients storage
        nabla_w = [None] * len(self.weights)
        nabla_b = [None] * len(self.biases)

        # Set output layer gradients
        nabla_w[-1] = np.dot(self.activations[-2].T, delta)
        nabla_b[-1] = np.sum(delta, axis=0, keepdims=True)

        # Propagate error backward
        for i in range(len(self.weights) - 2, -1, -1):
            delta = np.dot(delta, self.weights[i + 1].T) * self.sigmoid_derivative(
                self.z_values[i]
            )
            nabla_w[i] = np.dot(self.activations[i].T, delta)
            nabla_b[i] = np.sum(delta, axis=0, keepdims=True)

        # Update Weights and Biases (Gradient Descent)
        for i in range(len(self.weights)):
            self.weights[i] -= learning_rate * nabla_w[i]
            self.biases[i] -= learning_rate * nabla_b[i]

    def mutate(self, rate=0.1):
        """
        Randomly alters the weights (Genetic Algorithm style).
        """
        for i in range(len(self.weights)):
            self.weights[i] += np.random.randn(*self.weights[i].shape) * rate
