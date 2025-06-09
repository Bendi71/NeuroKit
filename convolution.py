import numpy as np

from .activation import Activation
from .layer import Layer

# FIXME: Fix backward propagation for Conv

class Conv(Layer):
    def __init__(self, input_shape: tuple[int, int, int], kernel_size: int, depth: int, activation: Activation):
        super().__init__()
        input_depth, input_height, input_width = input_shape
        self.depth = depth
        self.input_shape = input_shape
        self.input_depth = input_depth
        self.output_shape = (depth, input_height - kernel_size + 1, input_width - kernel_size + 1)
        self.kernels_shape = (depth, input_depth, kernel_size, kernel_size)
        self.kernels = np.random.random(self.kernels_shape)
        self.biases = np.random.random((self.depth, 1, 1))
        self.parameters = [self.kernels, self.biases]
        self.activation = activation

    def forward_propagation(self, input_data: np.ndarray):
        self.input = input_data
        self.z = self.convolve(self.input, self.kernels, self.biases)
        self.output = self.activation.forward_propagation(self.z)
        return self.output

    def backward_propagation(self, output_gradient, optimizer):
        activation_gradient = self.activation.backward_propagation(output_gradient)
        input_gradient = self.compute_gradient(activation_gradient, optimizer)
        return input_gradient

    def compute_gradient(self, output_gradient, optimizer):
        kernel_size = self.kernels.shape[2]

        biases_gradient = np.sum(output_gradient, axis=(0, 2, 3))[:, np.newaxis, np.newaxis] / (
                    self.input.shape[0] * self.input.shape[2] * self.input.shape[3])

        patches = self.extract_patches(self.input,
                                       kernel_size)
        output_gradient_exp = output_gradient[:, :, :, :, np.newaxis, np.newaxis]

        kernels_gradient = np.sum(
            patches[:, np.newaxis, :, :, :, :, :] * output_gradient_exp[:, :, np.newaxis, :, :, :, :], axis=(0, 3, 4)
        ) / (self.input.shape[0] * self.input.shape[2] * self.input.shape[3])

        flipped_kernels = np.flip(self.kernels, axis=(2, 3))
        flipped_kernels = np.expand_dims(flipped_kernels, axis=(0, 3, 4))

        padded_output_gradient = np.pad(output_gradient, (
            (0, 0), (0, 0), (kernel_size - 1, kernel_size - 1), (kernel_size - 1, kernel_size - 1)))

        grad_patches = self.extract_patches(padded_output_gradient, kernel_size)
        grad_patches = np.expand_dims(grad_patches, axis=2)

        input_gradient = np.sum(grad_patches * flipped_kernels, axis=(-2, -1))

        self.kernels = optimizer.update(self.kernels, kernels_gradient)
        self.biases = optimizer.update(self.biases, biases_gradient)

        return input_gradient

    def extract_patches(self, input_data, kernel_size):
        batch_size, input_depth, input_height, input_width = input_data.shape
        output_height = input_height - kernel_size + 1
        output_width = input_width - kernel_size + 1

        patches = np.lib.stride_tricks.as_strided(
            input_data,
            shape=(batch_size, input_depth, output_height, output_width, kernel_size, kernel_size),
            strides=(*input_data.strides[:2], input_data.strides[2], input_data.strides[3], *input_data.strides[2:]),
            writeable=False
        )

        return patches  # (batch_size, input_depth, output_height, output_width, kernel_size, kernel_size)

    def convolve(self, input_data, kernels, biases):
        patches = self.extract_patches(input_data,
                                       kernels.shape[2])  # (batch_size, input_depth, output_height, output_width, K, K)

        output = np.tensordot(patches, kernels,
                              axes=([1, 4, 5], [1, 2, 3]))  # (batch_size, output_height, output_width, output_depth)

        output = np.moveaxis(output, -1, 1)

        output += biases[np.newaxis, :, :, :]

        return output