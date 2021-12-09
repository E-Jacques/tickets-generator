from typing import List
import qrcode
from PIL import Image
from os import remove, listdir
from random import choice
from string import ascii_letters, digits

HASH_CHAR = ascii_letters + digits
WEBSITE_URL = "http://51.255.50.66:3001/"

def clear_qrcode_dir() -> None:
    for img in listdir("qrcode"):
        remove("qrcode/" + img)

    for img in listdir("temp_qrcode"):
        remove("temp_qrcode/" + img)

def copy_on_image(source: Image.Image, dest: Image.Image, x: int, y: int) -> Image.Image:
    for i in range(source.size[0]):
        for j in range(source.size[1]):
            # print(x+i, y+j)
            dest.putpixel((x + i, y + j), source.getpixel((i, j)))

    return dest

def compact_image(image_list: List[Image.Image], n_per_page: int, page_dim: List[int]) -> List[Image.Image]:
    n_of_page = (len(image_list) // n_per_page) + 1
    w, h = image_list[0].size
    page_list: List[Image.Image] = []

    for i in range(n_of_page):
        page_image = Image.new("RGB", page_dim)
        for j in range(n_per_page):
            idx = i * n_per_page + j
            if idx == len(image_list):
                break
            image = image_list[idx]
            # print((j % 2) * w, (j // 2) * h)
            copy_on_image(image, page_image, (j % 2) * w, (j // 2) * h)

        page_list.append(page_image)

    return page_list


def get_website_url(h: str) -> str:
    return WEBSITE_URL + h

def generate_hash(hash_length: int) -> str:
    s = ""
    for _ in range(hash_length):
        s += choice(HASH_CHAR)

    return s

def save_image_list(image_list: List[Image.Image], name_list: List[Image.Image]) -> None:
    for i in range(len(image_list)):
        image_list[i].save(name_list[i])

def add_qrcode_to_template(template_path: str, qrcode_img_path: str, save_path: str) -> Image.Image:
    template_img = Image.open(template_path)
    qrcode_img = Image.open(qrcode_img_path)

    for i in range(qrcode_img.size[0]):
        for j in range(qrcode_img.size[1]):
            c = qrcode_img.getpixel((i, j))
            template_img.putpixel((i, j), (255 * c, 255 * c, 255 * c))

    return template_img

def make_qrcode_from_url(path: str, url: str) -> None:
    img = qrcode.make(url)
    img.save(path)

def generate_qrcode(N: int, hash_length: int) -> None:
    hash_list = []
    image_list = []
    for _ in range(N):
        h = generate_hash(hash_length)
        hash_list.append(h)
        url = get_website_url(h)

        make_qrcode_from_url("./temp_qrcode/" + h + ".png", url)
        img = add_qrcode_to_template("./template.png", "./temp_qrcode/" + h + ".png", "./qrcode/" + h + ".png")
        image_list.append(img)

    save_image_list(image_list, list(map(lambda s: "qrcode/" + s + ".png", hash_list)))
    page_list = compact_image(image_list, 8, [1046, 1480])
    save_image_list(page_list, list(map(lambda s: "qrcode/" + s + "_page.png", [str(i) for i in range(len(page_list))])))

    
    with open("hash.txt", "w") as hash_file:
            hash_file.write("\n".join(hash_list))

if __name__ == "__main__":
    clear_qrcode_dir()
    generate_qrcode(50, 16)