import os
import glob
import hashlib
from datetime import datetime
from shutil import copy
from run_server import app
from models.photos import Gallery, Photo, CropSettings
from models.deploy import DeployedFiles
from utils import make_crop, get_image_info, get_orientation
from flask_frozen import Freezer
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import yaml


freezer = Freezer(app)

@freezer.register_generator
def home_view():
    for gallery in Gallery.query.all():
        yield {'gallery_key': gallery.key}


@freezer.register_generator
def photo_page_view():
    for gallery in Gallery.query.all():
        for photo in gallery.photos:
            yield {'gallery_key': gallery.key, 'photo_key': photo.key}


def create_deploy_list():
    """
    Checks the files in the Build folder against the DeployedFiles table. Returns a list of files
    that either don't exist in the table or have different hashes
    """
    build_list = []
    deploy_list = []
    file_i = 1
    for dirName, subdirList, fileList in os.walk(app.config["BUILD_DIR"]):
        for fname in fileList:
            build_list.append(os.path.join(dirName, fname))
    for build_file in build_list:
        fhash = hashlib.md5(open(build_file).read()).hexdigest()
        search_result = DeployedFiles.query.filter_by(path=build_file).first()
        if not search_result:
            deploy_list.append(build_file)
            print "File added to deploy list: %s" % build_file
        if search_result:
            fhash = hashlib.md5(open(build_file).read()).hexdigest()
            if fhash != search_result.hash:
                deploy_list.append(build_file)
                print "Changed file added to deploy list: %s" % build_file
    return deploy_list


def update_deployed_files(filename):
    fhash = hashlib.md5(open(filename).read()).hexdigest()
    file_doc = DeployedFiles.query.filter_by(path=filename).first()
    if not file_doc:
        file_doc = DeployedFiles(path=filename)
    print "file_doc.name: %s, file_doc.hash: %s" % (file_doc.path, fhash)
    file_doc.hash = fhash
    file_doc.save()
    return "File added to DeployedFiles table: %s" % filename


def build_site():
    freezer.freeze()


def deploy_site():
    file_i = 1
    conn = S3Connection(app.config["AWS_ACCESS_KEY"],app.config["AWS_SECRET_KEY"])
    bucket = conn.get_bucket(app.config["SITE_BUCKET"])
    deploy_list = create_deploy_list()
    for deploy_file in deploy_list:
        print "Deploying file %s of %s: %s" % (file_i, len(deploy_list), deploy_file)
        k = Key(bucket)
        k.key = deploy_file.replace(app.config["BUILD_DIR"]+"/",'')
        k.set_contents_from_file(open(deploy_file))
        file_i += 1
        update_deployed_files(deploy_file)


def import_files():
    file_types = ('*.jpg', '*.JPG')
    for directory in os.listdir(app.config["UPLOAD_DIR"]):
        photos = []
        if directory != '.DS_Store':
            gallery = Gallery(name=directory)
            gallery_dir = os.path.join(app.config["UPLOAD_DIR"], directory)
            for file_type in file_types:
                photos.extend(glob.glob(str(gallery_dir+"/"+file_type)))
            gallery.key = hashlib.sha512(str(photos[0])).hexdigest()[:7]
            photo_i = 1
            for photo in photos:
                copy(photo, app.config["PHOTO_STORE"])
                slash = photo.rfind('/')+1
                filename = photo[slash:]
                photo_doc = Photo(filename=filename)
                photo_exif = get_image_info(photo)
                if photo_exif is not None:
                    photo_doc.exif = str(photo_exif)
                    try:
                        year, month, dayhour, minute, second = str(photo_exif["DateTimeOriginal"]).split(':')
                        day, hour = dayhour.split(' ')
                        photo_doc.date_taken = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
                    except:
                        photo_doc.date_taken = datetime.now()
                photo_doc.key = hashlib.sha512(open(photo).read()).hexdigest()[:7]
                crop_i = 1
                crops = dict()
                for cropsetting in CropSettings.query.all():
                    cropfile = make_crop(filename, cropsetting.name, cropsetting.height, cropsetting.width)
                    print "Making crops - Crop[%s/%s] for Photo[%s/%s] Crop file: %s" \
                          % (crop_i, len(CropSettings.query.all()), photo_i, len(photos), cropfile)
                    crops[cropsetting.name] = cropfile
                    crop_i += 1
                photo_doc.crops = str(crops)
                photo_doc.orientation = get_orientation(os.path.join(app.config["PHOTO_STORE"], filename))
                photo_doc.save()
                gallery.photos.append(photo_doc)
                photo_i += 1
            if os.path.isfile(os.path.join(gallery_dir, "meta.yaml")):
                print "Desc.txt exists. Importing."
                #There's probably a million ways to do this better than I am doing right here.
                with open(os.path.join(gallery_dir, "meta.yaml"), "r") as desc_file:
                    try:
                        gallery.date = yaml.load(desc_file)["date"]
                    except:
                        print "No Date found in yaml"
                with open(os.path.join(gallery_dir, "meta.yaml"), "r") as desc_file:
                    try:
                        gallery.desc = yaml.load(desc_file)["desc"]
                    except:
                        print "No desc found in yaml"
            gallery.save()


def get_descriptions():
    for directory in os.listdir(app.config["UPLOAD_DIR"]):
        if directory != '.DS_Store':
            gallery = Gallery.query.filter_by(name=directory).first()
            gallery_dir = os.path.join(app.config["UPLOAD_DIR"], directory)
            if os.path.isfile(os.path.join(gallery_dir, "desc.txt")):
                print "Desc.txt exists. Importing."
                with open(os.path.join(gallery_dir, "desc.txt"), "r") as desc_file:
                    data = desc_file.read().replace('\n', '')
                    print "Desc.txt content: %s" % data
                    gallery.desc = data
            gallery.save()