import qrcode
import re
import io
import base64
from webcolors import rgb_to_hex
from PIL import Image


class QrCodeBase:
    def __init__(self,
            inputData: str,
            size: int,
            errorCorrection="30%",
            border=4,
            boxSize=10,
            version=None,
            fillColor="black",
            backColor="white",
            logo="",
            savePath=None):
        self.inputData = inputData
        self.size = int(size)
        self.errorCorrection = errorCorrection
        self.border = border
        self.boxSize = boxSize
        self.version = version
        self.fillColor = fillColor
        self.backColor = backColor
        self.logo = logo
        self.savePath = savePath

    def genQrCodePng(self):
        """生成png二维码"""
        pattern = re.compile(r"rgba\((?P<red>\d+), (?P<green>\d+), (?P<blue>\d+), (?P<transparent>\d+)\)")
        ret = re.search(pattern, self.backColor)
        if ret:
            red = int(ret.group('red'))
            green = int(ret.group('green'))
            blue = int(ret.group('blue'))
            transparent = ret.group('transparent')
            if transparent == '0':
                self.backColor = 'transparent'
            else:
                self.backColor = rgb_to_hex((red, green, blue))
        errorCorrectionDic = {
            "7%": qrcode.constants.ERROR_CORRECT_L,
            "15%": qrcode.constants.ERROR_CORRECT_M,
            "25%": qrcode.constants.ERROR_CORRECT_Q,
            "30%": qrcode.constants.ERROR_CORRECT_H,
        }

        qr = qrcode.QRCode(
            version=self.version,
            error_correction=errorCorrectionDic.get(self.errorCorrection, qrcode.constants.ERROR_CORRECT_H),
            box_size=self.boxSize,
            border=self.border,
        )
        qr.add_data(self.inputData)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fillColor, back_color=self.backColor)
        img = img.convert("RGBA")
        img = img.resize((self.size, self.size), Image.ANTIALIAS)

        if self.logo:  # 添加logo图片
            factor = 6
            # 对图片进行处理
            if isinstance(self.logo, str):
                logoBase64Data = base64.b64decode(self.logo.replace('data:image/png;base64,', ''))
                imageData = io.BytesIO(logoBase64Data)
                icon = Image.open(imageData)
            else:
                icon = Image.open(self.logo)
            iconW, iconH = icon.size
            imgW, imgH = img.size
            sizeW = int(imgW / factor)
            sizeH = int(imgH / factor)
            if iconW > sizeW:
                iconW = sizeW
            if iconH > sizeH:
                iconH = sizeH
            icon = icon.resize((iconW, iconH), Image.ANTIALIAS)  # 重新设置logo的尺寸

            middleWidth = int((imgW - iconW) / 2)  # logo居中位置的宽，高
            middleHeight = int((imgH - iconH) / 2)
            icon = icon.convert("RGBA")
            img.paste(icon, (middleWidth, middleHeight))
        print('====')
        if not self.savePath:
            buf = io.BytesIO()

            # plt.imshow(img)
            # plt.show()

            img.save(buf, format='PNG')
            image_stream = buf.getvalue()
            heximage = base64.b64encode(image_stream)
            return 'data:image/png;base64,' + heximage.decode()

        img.save(self.savePath)