from tool.generateQRcode import QrCodeBase
from tool.mosaicPictures import pictureSynthesis
from PIL import Image


if __name__ == '__main__':
    # 需要拼接图片的地址
    inputDicPath = "./EkIn8ZDVcAAJZrb.jpg"
    # 获取图片的尺寸
    img = Image.open(inputDicPath)
    size = int(int(img.size[0]) / 5)
    # 需要生成二维码的数据
    data = "涩图"
    # 保存二维码的路径
    qrcodePath = "./qrcode.png"
    # 使用代码生成二维码图片
    qrcode = QrCodeBase(data, size=size, savePath=qrcodePath).genQrCodePng()

    # 保存拼接图片的路径
    newPicPath = "./result.png"
    # 使用代码拼接图片
    pictureSynthesis(montherImg=inputDicPath, sonImg=qrcodePath, saveImg=newPicPath)