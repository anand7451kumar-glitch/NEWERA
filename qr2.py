import qrcode

text = input("Enter text or a URL: ").strip()

if not text:
    print("Error: Input cannot be empty.")
else:
    image = qrcode.make(text)
    image.save("my_qr.png")
    print("QR code saved as my_qr.png")