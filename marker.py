#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import math

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops

# TTF_FONT = u'./font/bird.ttf'
TTF_FONT = os.path.join("font", "bird.ttf")
TTF_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), TTF_FONT)


def add_mark(imagePath, mark, args):
    '''
    添加水印，然后保存图片
    '''
    im = Image.open(imagePath)
    # 判断图片是否为gif
    if im.format != 'GIF':
        image = mark(im)
        name = os.path.basename(imagePath)
        if image:
            if not os.path.exists(args.out):
                os.mkdir(args.out)

            new_name = os.path.join(args.out, name)
            if os.path.splitext(new_name)[1] != '.png':
                image = image.convert('RGB')
            image.save(new_name, quality=args.quality)

            print(name + " Success.")
        else:
            print(name + " Failed.")
    else:
        print("This is a gif image!")


def set_opacity(im, opacity):
    '''
    设置水印透明度
    '''
    assert opacity >= 0 and opacity <= 1

    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def crop_image(im):
    '''裁剪图片边缘空白'''
    bg = Image.new(mode='RGBA', size=im.size)
    diff = ImageChops.difference(im, bg)
    del bg
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im


def gen_mark(args):
    '''
    生成mark图片，返回添加水印的函数
    '''
    # 字体宽度
    width = len(args.mark) * args.size

    # 创建水印图片(宽度、高度)
    mark = Image.new(mode='RGBA', size=(width, args.size))

    # 生成文字
    draw_table = ImageDraw.Draw(im=mark)
    draw_table.text(xy=(0, 0),
                    text=args.mark,
                    fill=args.color,
                    font=ImageFont.truetype(TTF_FONT,
                                            size=args.size))
    del draw_table

    # 裁剪空白
    mark = crop_image(mark)

    # 透明度
    set_opacity(mark, args.opacity)

    def mark_im(im):
        ''' 在im图片上添加水印 im为打开的原图'''

        # 计算斜边长度
        c = int(math.sqrt(im.size[0]*im.size[0] + im.size[1]*im.size[1]))

        # 以斜边长度为宽高创建大图（旋转后大图才足以覆盖原图）
        mark2 = Image.new(mode='RGBA', size=(c, c))

        # 在大图上生成水印文字，此处mark为上面生成的水印图片
        y, idx = 0, 0
        while y < c:
            # 制造x坐标错位
            x = -int((mark.size[0] + args.space)*0.5*idx)
            idx = (idx + 1) % 2

            while x < c:
                # 在该位置粘贴mark水印图片
                mark2.paste(mark, (x, y))
                x = x + mark.size[0] + args.space
            y = y + mark.size[1] + args.space

        # 将大图旋转一定角度
        mark2 = mark2.rotate(args.angle)

        # 在原图上添加大图水印
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        im.paste(mark2,  # 大图
                 (int((im.size[0]-c)/2), int((im.size[1]-c)/2)),  # 坐标
                 mask=mark2.split()[3])
        del mark2
        return im

    return mark_im


def main():
    parse = argparse.ArgumentParser()
    # -f参数，输入图片的位置（可以是具体的一张照片，也可以是整个文件夹）
    parse.add_argument("-f", "--file", type=str,
                       help="image file path or directory")

    # -m参数，你要添加的内容
    parse.add_argument("-m", "--mark", type=str, help="watermark content")

    # -o 参数，指定输出水印文件的位置
    parse.add_argument("-o", "--out", default="./img",
                       help="image output directory, default is ./img")

    # -c 参数，指定水印的颜色
    parse.add_argument("-c", "--color", default="#232862", type=str,
                       help="text color like '#000000', default is #8B8B1B")

    # -s 参数，指定水印之间的空隙
    parse.add_argument("-s", "--space", default=100, type=int,
                       help="space between watermarks, default is 75")

    # -a 参数，指定水印的旋转角度
    parse.add_argument("-a", "--angle", default=30, type=int,
                       help="rotate angle of watermarks, default is 30")

    # --size参数，指定水印文本字体大小
    parse.add_argument("--size", default=50, type=int,
                       help="font size of text, default is 50")

    # --opacity参数，指定透明度，数值越小越透明
    parse.add_argument("--opacity", default=0.05, type=float,
                       help="opacity of watermarks, default is 0.15")

    # --quality参数，输出图像的质量
    parse.add_argument("--quality", default=80, type=int,
                       help="quality of output images, default is 90")

    args = parse.parse_args()

    if isinstance(args.mark, str) and sys.version_info[0] < 3:
        args.mark = args.mark.decode("utf-8")

    mark = gen_mark(args)

    if os.path.isdir(args.file):
        names = os.listdir(args.file)
        for name in names:
            image_file = os.path.join(args.file, name)
            add_mark(image_file, mark, args)
    else:
        add_mark(args.file, mark, args)


if __name__ == '__main__':
    main()
