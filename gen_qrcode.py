import qrcode
from PIL import Image
from os import remove, listdir
from random import choice
from string import ascii_letters, digits

HASH_CHAR = ascii_letters + digits
WEBSITE_URL = "http://51.255.50.66/"

def clear_qrcode_dir() -> None:
    for img in listdir("qrcode"):
        remove("qrcode/" + img)

    for img in listdir("temp_qrcode"):
        remove("temp_qrcode/" + img)

def get_website_url(h: str) -> str:
    return WEBSITE_URL + h

def generate_hash(hash_length: int) -> str:
    s = ""
    for _ in range(hash_length):
        s += choice(HASH_CHAR)

    return s

def add_qrcode_to_template(template_path: str, qrcode_img_path: str, save_path: str) -> None:
    template_img = Image.open(template_path)
    qrcode_img = Image.open(qrcode_img_path)
    for i in range(qrcode_img.size[0]):
        for j in range(qrcode_img.size[1]):
            c = qrcode_img.getpixel((i, j))
            template_img.putpixel((i, j), (255 * c, 255 * c, 255 * c))

    template_img.save(save_path)

def make_qrcode_from_url(path: str, url: str) -> None:
    img = qrcode.make(url)
    img.save(path)

def generate_qrcode(N: int, hash_length: int) -> None:
    hash_list = []
    for _ in range(N):
        h = generate_hash(hash_length)
        hash_list.append(h)
        url = get_website_url(h)

        make_qrcode_from_url("./temp_qrcode/" + h + ".png", url)
        add_qrcode_to_template("./template.png", "./temp_qrcode/" + h + ".png", "./qrcode/" + h + ".png")
    
    with open("hash.txt", "w") as hash_file:
            hash_file.write("\n".join(hash_list))

if __name__ == "__main__":
    clear_qrcode_dir()
    generate_qrcode(10, 16)