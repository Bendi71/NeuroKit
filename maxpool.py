import numpy as np

from .layer import Layer


class MaxPooling(Layer):
    def __init__(self, pool_size: int, stride: int):
        super().__init__()
        self.pool_size = pool_size
        self.stride = stride

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.pool(input_data, self.pool_size, self.stride)
        return self.output

    def backward_propagation(self, output_gradient, optimizer):
        input_gradient = self.compute_gradients(output_gradient)
        return input_gradient

    def pool(self, input_data, pool_size, stride):
        batch_size, depth, height, width = input_data.shape

        pooled_height = (height - pool_size) // stride + 1
        pooled_width = (width - pool_size) // stride + 1

        shape = (batch_size, depth, pooled_height, pooled_width, pool_size, pool_size)
        strides = (*input_data.strides[:2], stride * input_data.strides[2], stride * input_data.strides[3],
                   *input_data.strides[2:])
        windows = np.lib.stride_tricks.as_strided(input_data, shape=shape, strides=strides)

        return np.max(windows, axis=(4, 5))

    def compute_gradients(self, output_gradient):
        batch_size, depth, height, width = self.input.shape
        input_gradient = np.zeros_like(self.input)

        pooled_height = (height - self.pool_size) // self.stride + 1
        pooled_width = (width - self.pool_size) // self.stride + 1

        for i in range(pooled_height):
            for j in range(pooled_width):
                h_start, h_end = i * self.stride, i * self.stride + self.pool_size
                w_start, w_end = j * self.stride, j * self.stride + self.pool_size

                input_slice = self.input[:, :, h_start:h_end, w_start:w_end]

                max_pool = np.max(input_slice, axis=(2, 3), keepdims=True)
                mask = (input_slice == max_pool)

                input_gradient[:, :, h_start:h_end, w_start:w_end] += mask * output_gradient[:, :, i, j][:, :, None,
                                                                             None]

        return input_gradient