#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: virtual_printer.py
#    date: 2017-09-26
#  author: paul.dautry
# purpose:
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
# IMPORTS
#==============================================================================
import os
import io
from PIL        import Image
from PIL        import ImageDraw
from base64     import b64encode
from datetime   import datetime
#==============================================================================
# CLASSES
#==============================================================================
##
## @brief      Exception for signaling invalid ipv4 errors.
##
class InvalidIPv4Exception(Exception):
    pass
##
## @brief      Exception for signaling too many bytes errors.
##
class TooManyBytesException(Exception):
    pass
##
## @brief      Exception for signaling invalid dpi value errors.
##
class InvalidDPIValueException(Exception):
    pass
##
## @brief      Class for machine identification code.
##
class MachineIdentificationCode(object):
    ##
    ## @brief      Constructs the object.
    ##
    ## @param      ip    { parameter_description }
    ##
    def __init__(self, ip):
        super(MachineIdentificationCode, self).__init__()
        self.w = 64 # matrix width in dots
        self.h = 8 # matrix heights in dots
        self.oe = 50 # space between matrices
        self.od = 20 # space between dots
        self.mat = [ [ 1 for i in range(0, self.w) ] for i in range(0, self.h) ]
        self.sn = os.urandom(32)
        self.__prepare(ip)
    ##
    ## @brief      { function_description }
    ##
    ## @param      ip    { parameter_description }
    ##
    def __convert_ip(self, ip):
        digits = [ int(e) for e in ip.split('.') ]

        if len(digits) != 4:
            raise InvalidIPv4Exception

        for e in digits:
            if e > 0xff or e < 0:
                raise InvalidIPv4Exception

        return bytes(digits)
    ##
    ## @brief      Gets the datetime.
    ##
    def __get_datetime(self):
        t = datetime.now()
        y1 = t.year // 100
        y2 = t.year - y1 * 100
        return bytes([t.day, t.month, y1, y2, t.hour, t.minute, t.second])
    ##
    ## @brief      Sets the data.
    ##
    ## @param      data  The data
    ##
    def __set_data(self, data):
        if len(data) > self.w:
            raise TooManyBytesException

        for c in range(0, self.w):
            if c >= len(data):
                continue

            o = data[c]

            for r in range(0, self.h):
                if (o >> r) & 1 == 0:
                    self.mat[7-r][c] = 0
    ##
    ## @brief      { function_description }
    ##
    ## @param      ip    { parameter_description }
    ##
    def __prepare(self, ip):
        bip = self.__convert_ip(ip)
        bdate = self.__get_datetime()
        data = b'ip:'
        data += bip
        data += b'\nat:'
        data += bdate
        data += b'\nS/N:'
        data += self.sn
        data += b'\n'
        self.__set_data(data)
    ##
    ## @brief      { function_description }
    ##
    ## @param      rn    { parameter_description }
    ## @param      cn    { parameter_description }
    ##
    def __points_from_mat(self, rn, cn):
        points = []
        for r in range(0, self.h):
            for c in range(0, self.w):
                if self.mat[r][c] == 1:
                    x = c * self.od + self.oe + cn * (self.oe + self.w * self.od)
                    y = r * self.od + self.oe + rn * (self.oe + self.h * self.od)
                    points.append((x,y))
        return points
    ##
    ## @brief      { function_description }
    ##
    ## @param      img   The image
    ##
    def apply_on(self, img):
        (w, h) = img.size
        cc = w // (self.w * self.od + self.oe)
        rc = h // (self.h * self.od + self.oe)
        d = ImageDraw.Draw(img)
        for r in range(0, rc):
            for c in range(0, cc):
                points = self.__points_from_mat(r,c)
                d.point(points, fill=(255, 255, 204))
        return True
    ##
    ## @brief      { function_description }
    ##
    def b64sn(self):
        return b64encode(self.sn).decode()
##
## @brief      Class for A4 page.
##
class A4Page(object):
    SZ_PER_DPI = {
        300: (2480, 3508),
        200: (1654, 2339),
        100: (827, 1170),
        72: (596, 842)
    }
    WHITE = (255, 255, 255)
    ##
    ## @brief      Constructs the object.
    ##
    ## @param      margins  The margins
    ## @param      dpi      The dpi
    ##
    def __init__(self, margins, dpi=300):
        super(A4Page, self).__init__()
        (self.t, self.l, self.b, self.r) = margins
        if dpi not in A4Page.SZ_PER_DPI.keys():
            raise InvalidDPIValueException
        (self.w, self.h) = A4Page.SZ_PER_DPI[dpi]
        self.page = Image.new('RGB', A4Page.SZ_PER_DPI[dpi], A4Page.WHITE)
    ##
    ## @brief      { function_description }
    ##
    ## @param      mic   The mic
    ##
    def apply_mic(self, mic):
        return mic.apply_on(self.page)
    ##
    ## @brief      Sets the image.
    ##
    ## @param      img   The image
    ##
    def set_image(self, img):
        # resize image if necessary
        (w, h) = img.size
        cw = min(self.w / (w + self.l + self.r), 1.0)
        ch = min(self.h / (h * cw + self.t + self.b), 1.0)
        nw = int(w * cw * ch)
        nh = int(h * cw * ch)
        rimg = img.resize((nw, nh), Image.BICUBIC)
        # add image to page
        if len(rimg.split()) > 3:
            self.page.paste(rimg, (self.l, self.t), mask=rimg.split()[-1])
        else:
            self.page.paste(rimg, (self.l, self.t))
        return True
    ##
    ## @brief      { function_description }
    ##
    def data(self):
        data = io.BytesIO()
        self.page.save(data, format='png')
        return data
#==============================================================================
# FUNCTIONS
#==============================================================================
##
## @brief      { function_description }
##
## @param      img_bytes  The image bytes
## @param      ip         { parameter_description }
##
def print_img(img_bytes, ip):
    page = A4Page((25, 25, 25, 25), 300)
    mic = MachineIdentificationCode(ip)
    img = Image.open(io.BytesIO(img_bytes))
    if not page.set_image(img):
        return {
            'status': False,
            'error': 'invalid image. Try with another (RGB or RGBA) PNG file.'
        }
    if not page.apply_mic(mic):
        return {
            'status': False,
            'error': 'failed to apply mic.'
        }
    return {
        'status': True,
        'data': page.data().getvalue(),
        'b64sn': mic.b64sn()
    }
