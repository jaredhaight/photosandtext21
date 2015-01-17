import os
from flask import request, redirect, url_for, render_template, send_from_directory
from photosandtext21 import app
from models.photos import Gallery, Photo
from sqlalchemy import desc

@app.route('/media/photos/<path:filename>')
def photo_view(filename):
    return send_from_directory((os.path.join(os.getcwd(), 'media/photos')), filename)

@app.route('/media/crops/<path:filename>')
def crop_view(filename):
    if filename == "null":
        return redirect('http://placekitten.com/g/800/600', 301)
    return send_from_directory((os.path.join(os.getcwd(), 'media/crops')), filename)

@app.route('/')
@app.route('/page/<int:page_num>/')
def home_view(page_num=1):
    site_url = "http://"+app.config["SITE_BUCKET"]
    galleries = Gallery.query.order_by(desc(Gallery.date)).paginate(per_page=12, page=page_num)
    return render_template('home.html', galleries=galleries, site_url=site_url)

@app.route('/gallery/<string:gallery_key>/')
def gallery_view(gallery_key):
    site_url = "http://"+app.config["SITE_BUCKET"]
    gallery = Gallery.query.filter_by(key=gallery_key).first_or_404()
    photos = gallery.photos.order_by(Photo.date_taken)
    return render_template('gallery.html', gallery=gallery, photos=photos, site_url=site_url)

@app.route('/gallery/<gallery_key>/photo/<photo_key>/')
def photo_page_view(gallery_key, photo_key):
    site_url = "http://"+app.config["SITE_BUCKET"]
    photo = Photo.query.filter_by(key=photo_key).first_or_404()
    gallery = Gallery.query.filter_by(key=gallery_key).first_or_404()
    pos = gallery.photos.order_by(Photo.date_taken).all().index(photo)
    paged = gallery.photos.order_by(Photo.date_taken).paginate(pos+1, per_page=1)
    try:
        aperture1, aperture2 = photo.get_exif("FNumber")
        photo_aperture = aperture1/float(aperture2)
    except:
        photo_aperture = None
    try:
        exif_a, exif_b = photo.get_exif('ExposureTime')
        if exif_b == 1:
            photo_shutter = '%s seconds' % exif_a
        else:
            photo_shutter = '%s/%s' % (exif_a, exif_b)
    except:
        photo_shutter = None
    try:
        focal_a, focal_b = photo.get_exif("FocalLength")
        photo_focal = focal_a/focal_b
    except:
        photo_focal = None
    return render_template('photo.html', photo=photo, photo_aperture=photo_aperture, photo_shutter=photo_shutter,
                           photo_focal=photo_focal, paged=paged, gallery=gallery, site_url=site_url)

@app.route('/about/')
def about_view():
    return render_template('about.html')
