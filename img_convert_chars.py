from PIL import Image
from random import shuffle
import os

MAX_WIDTH = 250
MAX_HEIGHT = 250

ASCII_CHAR = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# shuffle(ASCII_CHAR)
# print(ASCII_CHAR)

def resize(img):
    w, h = img.size
    if w > MAX_WIDTH:
        h = MAX_WIDTH / w * h
        w = MAX_WIDTH

    if h > MAX_HEIGHT:
        w = MAX_HEIGHT / h * w
        h = MAX_HEIGHT

    return img.resize((int(w), int(h)), Image.NEAREST)

# 将256灰度映射到70个字符上
def get_char(r, g, b, alpha=256):
    # 判断 alpha 值
    if alpha == 0:
        return ' '
    # 获取字符集的长度
    length = len(ASCII_CHAR)
    # 将 RGB 值转为灰度值 gray，灰度值范围为 0-255
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ASCII_CHAR[int(gray / unit)]

def convert_jpg(img_path):
    # 修改图片大小
    img_pic = resize(Image.open(img_path))
    img_name = os.path.basename(img_path)

    print(img_name)

    out_file = './result_chars_' + img_name.split('.')[0] + '.txt'
    print(out_file)

    if os.path.exists(out_file):
        os.remove(out_file)

    width, height = img_pic.size
    print(width, height)

    txt = ''
    for h in range(height):
        for w in range(width):
            if img_pic.mode == 'RGB':
                r, g, b = img_pic.getpixel((w, h))
            elif img_pic.mode == 'RGBA':
                r, g, b, a = img_pic.getpixel((w, h))
            # 将 (j,i) 坐标的 RGB 像素转为字符后添加到 txt 字符串
            txt += get_char(r=r, g=g, b=b)
        txt += '\n'

    with open(out_file, mode='w') as f:
        f.write(txt)

    print('success!')


if __name__ == '__main__':
    convert_jpg('Logo-2.png')
