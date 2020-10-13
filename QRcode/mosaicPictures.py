from PIL import Image, ImageDraw, ImageFont
from django.conf import settings


def pictureSynthesis(montherImg, sonImg, saveImg, coordinate=None):
    """
    :param montherImg: 母图
    :param sonImg: 子图
    :param saveImg: 保存图片名
    :param coordinate: 子图在母图的坐标
    :return:
    """
    # 用户上传的图片
    mImg = Image.open(montherImg)
    # 需要拼接的二维码图片
    sImg = Image.open(sonImg)
    # 打开绿色勾的图片
    greedImg = Image.open(settings.STATICFILES_DIRS[0]+'/ico_choice.png').convert('RGBA')
    # 打开章图片
    zhangImg = Image.open(settings.STATICFILES_DIRS[0]+'/章.png').convert('RGBA')

    # 给图片指定色彩显示格式
    mImg = mImg.convert("RGBA")
    mImg_w, mImg_h = mImg.size  # 获取被放图片的大小（母图）
    sImg_w, sImg_h = sImg.size  # 获取小图的大小（子图）

    # 生成一张在底端的白色背景图片
    backImage = Image.new('RGB', (mImg_w, sImg_h), "white")
    # 在这张白色背景图中写入内容
    draw = ImageDraw.Draw(backImage)

    # 字体位置基准
    textHeight = sImg_h * (1/7)
    # 写第一行的位置为
    titleLocation = (sImg_w * 1.2, textHeight * 1)
    # 写第二行的位置
    renzheng = (sImg_w * 1.2, textHeight * 3)
    # 写在第三行的位置

    # 将绿色的勾重新设置大小
    greedImg = greedImg.resize((int(textHeight), int(textHeight)), Image.ANTIALIAS)
    # 将绿色的章重新设置大小
    zhangImg = zhangImg.resize((int(sImg_w), int(sImg_w)), Image.ANTIALIAS)

    # 字体样式
    textFont = ImageFont.truetype(settings.STATICFILES_DIRS[0]+'/STHeiti Light.ttc', int(textHeight))

    draw.text(titleLocation, "水印打卡相机", "black", textFont)
    draw.text(renzheng, "认证编号：xxxxxxxxxxxxxxxxxxx", "black", textFont)
    draw.text((sImg_w * 1.2 + 2 * textHeight, textHeight * 5), "北京时间", "black", textFont)
    draw.text((sImg_w * 1.2 + 8 * textHeight, textHeight * 5), "定位认证", "black", textFont)
    draw.text((sImg_w * 1.2 + 14 * textHeight, textHeight * 5), "真实打卡", "black", textFont)
    # 将写了字的白色背景左边贴上二维码图片
    backImage.paste(sImg, (0, 0), mask=None)
    # 贴上绿色的勾的图片
    r, g, b, a = greedImg.split()
    backImage.paste(greedImg, (int(sImg_w * 1.2 + 0.5 * textHeight), int(textHeight * 5)), mask=a)
    backImage.paste(greedImg, (int(sImg_w * 1.2 + 6.5 * textHeight), int(textHeight * 5)), mask=a)
    backImage.paste(greedImg, (int(sImg_w * 1.2 + 12.5 * textHeight), int(textHeight * 5)), mask=a)

    # 将上传图片与生成图片进行拼接
    resultImg = Image.new('RGB', (mImg_w, mImg_h+sImg_h), "white")
    resultImg.paste(mImg, (0, 0), mask=None)
    resultImg.paste(backImage, (0, mImg_h), mask=None)

    # 打上印章
    r, g, b, a = zhangImg.split()
    resultImg.paste(zhangImg, (mImg_w-sImg_h, int(mImg_h-0.5*sImg_h)), mask=a)

    resultImg.save(saveImg)
