from .layer import Layer


class Reshape(Layer):
    def __init__(self, target_shape: tuple):
        super().__init__()
        self.target_shape = target_shape

    def forward_propagation(self, input_data):
        self.input_shape = input_data.shape
        self.output = input_data.reshape(self.target_shape)
        return self.output

    def backward_propagation(self, output_gradient):
        return output_gradient.reshape(self.input_shape)


class Flatten(Layer):
    def __init__(self):
        super().__init__()

    def forward_propagation(self, input_data):
        self.input_shape = input_data.shape
        batch_size = self.input_shape[0]
        self.output = input_data.reshape(batch_size, -1)
        return self.output

    def backward_propagation(self, output_gradient, optimizer):
        return output_gradient.reshape(self.input_shape)
