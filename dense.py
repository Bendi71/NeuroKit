import numpy as np

from .activation import Activation
from .layer import Layer
from .regularizer import Regularizer


class Dense(Layer):
    def __init__(self, output_size: int, activation: Activation = None, regularizer: Regularizer = None):
        super().__init__()
        self.output_shape = output_size
        self.weights = None
        self.biases = np.zeros((1, self.output_shape))
        self.activation = activation
        self.regularizer = regularizer
        self.biases_gradient = None
        self.weights_gradient = None
        self.parameters = [self.weights, self.biases]

    def forward_propagation(self, input_data):
        self.input = input_data
        self.input_shape = input_data.shape
        if self.weights is None:
            self.weights = np.random.rand(self.output_shape, self.input_shape[1])
        self.z = np.dot(self.input, self.weights.T) + self.biases
        self.output = self.activation.forward_propagation(self.z) if self.activation else self.z
        return self.output

    def backward_propagation(self, output_gradient, optimizer):
        activation_gradient = self.activation.backward_propagation(
            output_gradient) if self.activation else output_gradient
        self.weights_gradient = np.dot(activation_gradient.T, self.input) / self.input.shape[0]
        self.biases_gradient = np.sum(activation_gradient, axis=0, keepdims=True) / self.input.shape[0]

        if self.regularizer:
            self.weights_gradient += self.regularizer.gradient(self.weights)

        input_gradient = np.dot(activation_gradient, self.weights)
        self.weights = optimizer.update(self.weights, self.weights_gradient)
        self.biases = optimizer.update(self.biases, self.biases_gradient)
        self.parameters = [self.weights, self.biases]

        return input_gradient