import qrcode

with open('profile_links.txt','r') as file:
    for i in file:
        data = i.strip('\n')
        fast, rest = data.split('.', 1)
        data = rest.split('-', 1)
        img = qrcode.make(f"{data[1]}")
        img.save(f"{data[0]}.jpg")