from PIL import Image, ImageDraw
from coursework.filters import liner_filters, liner_filter_apply, red_filter, mono_filter, no_gray_filter, median_filter, swap_color_filter, green_filter


pic_name = "pic4"

image = Image.open(pic_name + ".png")
rgb_image = image.convert('RGB')


def prepare_image(image):
    pix = image.load()
    image_draw = ImageDraw.Draw(image)
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.

    buf1_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    buf1_draw = ImageDraw.Draw(buf1_image)
    buf1_pix = buf1_image.load()

    buf2_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    buf2_draw = ImageDraw.Draw(buf2_image)
    buf2_pix = buf2_image.load()

    # liner_filter_apply(buf1_draw, pix, width, height, liner_filters['max blur'])
    median_filter(buf1_draw, pix, width, height, 2)
    red_filter(buf1_draw, buf1_pix, width, height)
    green_filter(buf1_draw, buf1_pix, width, height, (0, 36, 243))
    liner_filter_apply(buf2_draw, buf1_pix, width, height, liner_filters['grad'])
    buf2_pix = buf2_image.load()
    no_gray_filter(buf1_draw, buf2_pix, width, height)
    buf1_pix = buf1_image.load()
    liner_filter_apply(buf2_draw, buf1_pix, width, height, liner_filters['copy'])
    pix = buf2_image.load()
    mono_filter(buf2_draw, pix, width, height)
    swap_color_filter(buf2_draw, pix, width, height, (255, 255, 255), (0, 0, 0))
    pix = buf2_image.load()
    median_filter(image_draw, pix, width, height, 3)

    buf1_image.show()
    buf2_image.show()
    image.show()

    del image_draw
    del buf1_draw
    del buf2_draw


prepare_image(rgb_image)


rgb_image.save(pic_name + "_prepared.png")