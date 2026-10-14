import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

# Load the saved model
saved = np.load("digit_model.npz")
W1, b1 = saved["W1"], saved["b1"]
W2, b2 = saved["W2"], saved["b2"]


def predict_digit(image):
    # Find the actual boundaries of the white digit
    image = image.convert("L")
    bbox = image.getbbox()

    if bbox is None:
        return [(None, 0.0)]

    image = image.crop(bbox)

    # Resize while preserving the digit's proportions
    image.thumbnail((6, 6))

    # Place it in the center of an 8x8 image
    canvas = Image.new("L", (8, 8), 0)

    x = (8 - image.width) // 2
    y = (8 - image.height) // 2

    canvas.paste(image, (x, y))

    # Match the training data's white digit on dark background
    pixels = np.array(canvas, dtype=float).reshape(1, 64) / 255.0

    # Forward propagation
    hidden = np.maximum(0, pixels @ W1 + b1)
    scores = hidden @ W2 + b2

    scores -= np.max(scores, axis=1, keepdims=True)
    probabilities = np.exp(scores)
    probabilities /= np.sum(probabilities, axis=1, keepdims=True)

    # Return the three most likely digits
    top_indices = np.argsort(probabilities[0])[::-1][:3]

    return [
        (int(i), float(probabilities[0, i] * 100))
        for i in top_indices
    ]


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
    try:
        guesses = predict_digit(drawing)

        if guesses[0][0] is None:
            result.config(text="Draw a digit first!")
            return

        lines = ["Top predictions:"]

        for digit, confidence in guesses:
            lines.append(f"{digit}: {confidence:.1f}%")

        result.config(text="\n".join(lines))

    except Exception as e:
        result.config(text=f"Error: {e}")
        print("Prediction error:", e)

def clear():
    canvas.delete("all")
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=0)
    result.config(text="Draw a digit from 0 to 9")


canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", paint)

tk.Button(root, text="Predict", command=predict).pack(pady=5)
tk.Button(root, text="Clear", command=clear).pack(pady=5)

result = tk.Label(
    root,
    text="Draw a digit from 0 to 9",
    font=("Arial", 14),
    justify="center",
    width=28,
    height=4
)
result.pack(pady=10)

root.mainloop()