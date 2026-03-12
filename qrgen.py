import qrcode

base_url = "http://172.20.10.3:8000/myapp/order/?table="

for table in range(1,6):

    url = base_url + str(table)

    img = qrcode.make(url)

    img.save(f"table_{table}.png")

print("QR codes generated!")