from PIL import Image

file = input("Image file: ")
width = int(input("New width: "))

image = Image.open(file)

ratio = width / image.width
height = int(image.height * ratio)

image.resize((width, height)).save("resized.jpg")

print("Saved as resized.jp")
