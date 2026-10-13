import numpy as np 
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits

# =================================
# 1. LOAD HANDWRITTEN DIGIT IMAGES
# =================================

digits = load_digits()

X = digits.data / 16.0
labels = digits.target

#Convert digit labels into 10 output values
y = np.eye(10)[labels]

#Shuffle the data
np.random.seed(42)
indices = np.random.permutation(len(X))
X = X[indices]
y = y[indices]
labels = labels[indices]

#Split into training and testing data
split = int(0.8 * len(X))

X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
labels_test = labels[split:]

print("TRAINING DATA:", X_train.shape)
print("TESTING DATA:", X_test.shape)

# ==============================
# 2. BUILD A NEURAL NETWORK FROM SCRATCH
# ==============================

class NeuralNetwork:
    def __init__(self):
        #64 inputs -> 32 hidden neurons -> 10 outputs
        self.W1 = np.random.randn(64, 32) * np.sqrt(2 / 64)
        self.b1 = np.zeros((1, 32))

        self.W2 = np.random.randn(32, 10) * np.sqrt(2 / 32)
        self.b2 = np.zeros((1, 10))

    def relu(self, z):
        return np.maximum(0, z)
    def relu_derivative(self, z):
        return (z > 0).astype(float)

    def softmax(self, z):
        z = z - np.max(z, axis=1, keepdims=True)
        exp_z = np.exp(z)
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)

        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.softmax(self.z2)

        return self.a2

    def train_step(self, X, y, learning_rate=0.1):
        batch_size = len(X)

        predictions = self.forward(X)

        #Backpropagation: calculate output-layer gradients
        dz2 = (predictions - y) / batch_size
        dW2 = self.a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        #Backpropagation: calculate hidden-layer gradients
        dz1 = (dz2 @ self.W2.T) * self.relu_derivative(self.z1)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        #Update weights and biases
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1

    def predict(self, X):
        probabilities = self.forward(X)
        return np.argmax(probabilities, axis=1)


# ==============================
# 3. TRAIN THE NETWORK
# ==============================

np.random.seed(1)
model = NeuralNetwork()

epochs = 1000
batch_size = 32

print("\nTRAINING NEURAL NETWORK")
print("=" * 40)

for epoch in range(epochs):
    order = np.random.permutation(len(X_train))

    for start in range(0, len(X_train), batch_size):
        batch_indices = order[start:start + batch_size]

        model.train_step(
            X_train[batch_indices],
            y_train[batch_indices]
        )

    if (epoch + 1) % 100 == 0:
        predictions = model.forward(X_train)
        loss = -np.mean(
            np.sum(y_train * np.log(predictions + 1e-9), axis=1)

        )

        accuracy = np.mean(
            np.argmax(predictions, axis=1)
            == np.argmax(y_train, axis=1)
        )

        print(
            f"Epoch {epoch + 1:4d} |"
            f"Loss: {loss:.4f} | "
            f"Accuracy: {accuracy * 100:.2f}%"
        )

# ==========================
# 4. TEST THE NETWORK
# ==========================

predictions = model.predict(X_test)
accuracy = np.mean(predictions == labels_test)

print("\nTEST RESULTS")
print("=" * 40)
print(f"Test accuracy: {accuracy * 100:.2f}%")

for i in range(10):
    print(
        f"Actual: {labels_test[i]} | "
        f"Predicted: {predictions[i]} | "
        f"{'CORRECT' if labels_test[i] == predictions[i] else 'WRONG'}"

    )

# ==========================
# 5. DISPLAY A PREDICTION
# ==========================

index = 0

plt.imshow(
    X_test[index].reshape(8, 8),
    cmap="gray_r",
    interpolation="nearest"
)

plt.title(
    f"Actual: {labels_test[index]} | "
    f"AI prediction: {predictions[index]}"

)

plt.axis("off")
plt.show()
