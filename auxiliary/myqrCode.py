import qrcode

qr = qrcode.QRCode()
qr.add_data("1;50")

im = qr.make_image()
im.save()