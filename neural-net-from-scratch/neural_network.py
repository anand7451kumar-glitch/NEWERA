import numpy as np

#Make the results reproducible
np.random.seed(42)

#XOR dataset:
#The network must learn these 4 examples.
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=float)

y = np.array([
    [0],
    [1],
    [1],
    [0]
], dtype=float)

y = np.array([
    [0],
    [1],
    [1],
    [0]
], dtype=float)

class NeuralNetwork:
    def __init__(self):
        #2 input neurons -> 4 hidden neurons -> 1 output neuron
        self.W1 = np.random.randn(2, 4) * 0.5
        self.b1 = np.zeros((1, 4))

        self.W2 = np.random.randn(4, 1) * 0.5
        self.b2 = np.zeros((1, 1))

    def sigmoid(self, z):
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def sigmoid_derivative(self, a):
        return a * (1 - a)

    def forward(self, X):
        #Input -> hidden layer
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.sigmoid(self.z1)

        #Hidden layer -> output
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.sigmoid(self.z2)

        return self.a2

    def train(self, X, y, epochs=20000, learning_rate=1.0):
        for epoch in range(epochs):
            #1. Forward propagation
            predictions = self.forward(X)

            #2. Calculate prediction error
            error = predictions - y
            loss = np.mean(error ** 2)

            #3. backpropagation
            d_output = (
                2 * error / len(X)
            ) * self.sigmoid_derivative(self.a2)

            d_W2 = self.a1.T @ d_output
            d_b2 = np.sum(d_output, axis=0, keepdims=True)

            d_hidden = (
                d_output @ self.W2.T
            ) * self.sigmoid_derivative(self.a1)

            d_W1 = X.T @ d_hidden
            d_b1 = np.sum(d_hidden, axis=0, keepdims=True)

            #4. Update weights and biases
            self.W2 -= learning_rate * d_W2
            self.b2 -= learning_rate * d_b2

            self.W1 -= learning_rate * d_W1
            self.b1 -= learning_rate * d_b1

            if (epoch + 1) % 2000 == 0:
                print(
                    f"Epoch {epoch + 1:5d} | "
                    f"Loss: {loss:.6f}"
                )

    def predict(self, X):
        return self.forward(X)


#Build and train the network
model = NeuralNetwork()

print("TRAINING NEURAL NETWORK")
print("=" * 35)

model.train(X, y)

#Test the network on all four examples.
print("\nPREDICTIONS")
print("=" * 35)

predictions = model.predict(X)

for inputs, prediction, expected in zip(X, predictions, y):
    predicted_class = int(prediction[0] >= 0.5)

    print(
        f"Input: {inputs.astype(int)} | "
        f"Output: {prediction[0]:.4f} | "
        f"Predicted: {predicted_class} | "
        f"Expected: {int(expected[0])}"
    )



