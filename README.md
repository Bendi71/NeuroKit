# NeuroKit

A lightweight neural network library for Python, providing essential building blocks for creating and training neural networks.

## Features

- Various activation functions
- Convolutional layers
- Dense (fully connected) layers
- Max pooling layers
- Reshape layers
- Loss functions and metrics
- Optimization algorithms
- Early stopping functionality
- Regularization techniques

## Installation

```bash
pip install neurokit
```

## Quick Start

```python
from neurokit import NeuralNetwork, Dense, Conv, MaxPooling, Reshape
from neurokit.activations import relu, softmax
from neurokit.losses import categorical_crossentropy
from neurokit.optimizer import Adam

# Create a simple CNN
model = NeuralNetwork()
model.add(Conv(32, (3, 3), activation=relu, input_shape=(28, 28, 1)))
model.add(MaxPooling((2, 2)))
model.add(Reshape((-1,)))
model.add(Dense(128, activation=relu))
model.add(Dense(10, activation=softmax))

# Compile the model
model.compile(loss=categorical_crossentropy, optimizer=Adam(learning_rate=0.001))

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {loss}, Test accuracy: {accuracy}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License
