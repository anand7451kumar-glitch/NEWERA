import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

# Load the saved model
saved = np.load("digit_model.npz")
W1, b1 = saved["W1"], saved["b1"]
W2, b2 = saved["W2"], saved["b2"]


def predict_digit(image):
    image = image.resize((8, 8)).convert("L")
    image = Image.eval(image, lambda p: 255 - p)
    pixels = np.array(image, dtype=float).reshape(1, 64) / 255.0

    hidden = np.maximum(0, pixels @ W1 + b1)
    scores = hidden @ W2 + b2
    scores -= np.max(scores, axis=1, keepdims=True)
    probabilities = np.exp(scores)
    probabilities /= np.sum(probabilities, axis=1, keepdims=True)

    digit = int(np.argmax(probabilities))
    return digit, probabilities[0, digit] * 100


WIDTH = HEIGHT = 280
root = tk.Tk()
root.title("My AI Digit Recognizer")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack(padx=10, pady=10)

drawing = Image.new("L", (WIDTH, HEIGHT), 0)
draw = ImageDraw.Draw(drawing)


def paint(event):
    x, y = event.x, event.y
    r = 12
    canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="white")
    draw.ellipse((x-r, y-r, x+r, y+r), fill=255)


def predict():
    digit, confidence = predict_digit(drawing)
    result.config(text=f"AI predicts: {digit} | Confidence: {confidence:.1f}%")


def clear():
    canvas.delete("all")
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=0)
    result.config(text="Draw a digit from 0 to 9")


canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", paint)

tk.Button(root, text="Predict", command=predict).pack(pady=5)
tk.Button(root, text="Clear", command=clear).pack(pady=5)

result = tk.Label(root, text="Draw a digit from 0 to 9", font=("Arial", 14))
result.pack(pady=10)

root.mainloop()