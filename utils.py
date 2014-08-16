import os

from PIL import Image, ImageOps
from PIL.ExifTags import TAGS

from photosandtext21 import app
from models.photos import CropSettings

PHOTO_STORE = app.config["PHOTO_STORE"]
CROP_STORE = app.config["CROP_STORE"]


def init_env():
    crop_list = list()
    crop_list.append(CropSettings(name="thumb200", height=200, width=200))
    crop_list.append(CropSettings(name="thumb400", height=400, width=400))
    crop_list.append(CropSettings(name="home400", height=0, width=400))
    crop_list.append(CropSettings(name="home600", height=0, width=600))
    crop_list.append(CropSettings(name="home800", height=0, width=800))
    crop_list.append(CropSettings(name="display1280", height=0, width=1280))
    crop_list.append(CropSettings(name="display1600", height=0, width=1600))
    crop_list.append(CropSettings(name="display_t", height=0, width=100))
    crop_list.append(CropSettings(name="display_m", height=0, width=240))
    crop_list.append(CropSettings(name="display_n", height=0, width=320))
    crop_list.append(CropSettings(name="display", height=0, width=500))
    crop_list.append(CropSettings(name="display_z", height=0, width=640))
    crop_list.append(CropSettings(name="display_c", height=0, width=800))
    crop_list.append(CropSettings(name="display_b", height=0, width=1024))
    for crop_setting in crop_list:
        crop_setting.save()


def get_orientation(image_filepath):
        image = Image.open(image_filepath)
        width, height = image.size

        if width > height:
            return 'landscape'

        if width < height:
            return 'portrait'


def make_crop(image, cropName, height, width):
    slash = image.find('/')+1
    dot = image.find('.')
    filename = image[slash:dot]+'_'+cropName+'.jpg'
    t_img = Image.open(PHOTO_STORE+"/"+image)
    if width > t_img.size[0]:
        width = t_img.size[0]
    if height > t_img.size[1]:
        height = t_img.size[1]
    if width == 0:
        width = t_img.size[0] * height / t_img.size[1]
        t_img.thumbnail((width,height), Image.ANTIALIAS)
        t_img.save(CROP_STORE+'/'+filename, 'JPEG', quality=90)
        return filename
    if height == 0:
        height = t_img.size[1] * width / t_img.size[0]
        t_img.thumbnail((width,height), Image.ANTIALIAS)
        t_img.save(CROP_STORE+'/'+filename, 'JPEG', quality=90)
        return filename
    t_fit = ImageOps.fit(t_img, (height,width), Image.ANTIALIAS, 0, (0.5,0.5))
    t_fit.save(CROP_STORE+'/'+filename,"JPEG", quality=90)
    #upload_to_cdn(filename,'crop')
    return filename


def get_image_info(image):
    ret = {}
    i = Image.open(image)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if type(decoded) is str and decoded is not "GPSInfo" and decoded is not "MakerNote":
            ret[decoded] = value
    return dict(ret)