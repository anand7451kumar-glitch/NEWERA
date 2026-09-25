import qrcode

text = input("Enter text or URL: ")

qr = qrcode.make(text)
qr.save("qr_code.png")

print("QR code saved as qr_code.png")