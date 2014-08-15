import os
import glob
import hashlib
from shutil import copy
from run_server import app
from models.photos import Gallery, Photo, CropSettings
from utils import make_crop, get_image_info
from flask_frozen import Freezer
from boto.s3.connection import S3Connection
from boto.s3.key import Key


freezer = Freezer(app)

@freezer.register_generator
def home_view():
    for gallery in Gallery.objects:
        yield {'gallery_id': gallery.id}

@freezer.register_generator
def photo_page_view():
    for photo in Photo.objects:
        yield {'photo_id': photo.id}

def build_site():
    freezer.freeze()

def deploy_site():
    conn = S3Connection(app.config["AWS_ACCESS_KEY"],app.config["AWS_SECRET_KEY"])
    bucket = conn.get_bucket(app.config["SITE_BUCKET"])
    deploy_list = []
    file_i = 1
    for dirName, subdirList, fileList in os.walk(app.config["BUILD_DIR"]):
        for fname in fileList:
            deploy_list.append(os.path.join(dirName,fname))
    for deploy_file in deploy_list:
        fhash = hashlib.md5(open(deploy_file).read()).hexdigest()
        print "Deploying file %s of %s: %s" % (file_i, len(deploy_list), deploy_file)
        k = Key(bucket)
        k.key = deploy_file.replace(app.config["BUILD_DIR"]+"/",'')
        k.set_contents_from_file(open(deploy_file))
        file_i = file_i + 1

def import_files():
    for directory in os.listdir(app.config["UPLOAD_DIR"]):
        gallery = Gallery(name=directory)
        gallery_dir = os.path.join(app.config["UPLOAD_DIR"],directory)
        photos = glob.glob(str(gallery_dir+"/*.jpg"))
        photo_i = 1
        for photo in photos:
            copy(photo, app.config["PHOTO_STORE"])
            slash = photo.rfind('/')+1
            filename = photo[slash:]
            photo_doc = Photo(filename=filename)
            photo_exif = get_image_info(photo)
            if photo_exif is not None:
                photo_doc.exif = photo_exif
            crop_i = 1
            for cropsetting in CropSettings.objects:
                cropfile = make_crop(filename, cropsetting.name, cropsetting.height, cropsetting.width)
                print "Making crops - Crop[%s/%s] for Photo[%s/%s] Crop file: %s" % (crop_i, len(CropSettings.objects), photo_i, len(photos), cropfile)
                photo_doc.crops[cropsetting.name] = cropfile
                photo_doc.save()
                crop_i = crop_i + 1
            photo_doc.save()
            gallery.photos.append(photo_doc)
            photo_i = photo_i+1
        if os.path.isfile(os.path.join(gallery_dir,"desc.txt")):
            with open(os.path.join(gallery_dir,"desc.txt"), "r") as desc_file:
                data = desc_file.read().replace('\n', '')
                gallery.description = data
        gallery.save()