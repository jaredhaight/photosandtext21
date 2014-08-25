import os
from flask import request, redirect, url_for, render_template, send_from_directory
from photosandtext21 import app
from models.photos import Gallery, Photo

if app.config['DEBUG']:
    @app.route('/media/photos/<path:filename>')
    def photo_view(filename):
        return send_from_directory((os.path.join(os.getcwd(), 'media/photos')), filename)

    @app.route('/media/crops/<path:filename>')
    def crop_view(filename):
        return send_from_directory((os.path.join(os.getcwd(), 'media/crops')), filename)

@app.route('/')
@app.route('/page/<int:page_num>/')
def home_view(page_num=1):
    galleries = Gallery.objects.paginate(per_page=12, page=page_num)
    return render_template('home.html', galleries=galleries)

@app.route('/gallery/<string:gallery_key>/')
def gallery_view(gallery_key):
    gallery = Gallery.objects.get_or_404(key=gallery_key)
    return render_template('gallery.html', gallery=gallery)

@app.route('/gallery/<gallery_key>/photo/<photo_key>/')
def photo_page_view(gallery_key, photo_key):
    photo = Photo.objects.get_or_404(key=photo_key)
    gallery = Gallery.objects.get_or_404(key=gallery_key)
    pos = gallery.photos.index(photo)
    paged = Gallery.objects.paginate_field('photos', gallery.id, pos+1, per_page=1)
    try:
        aperture1, aperture2 = photo.exif["FNumber"]
        photo_aperture = aperture1/float(aperture2)
    except:
        photo_aperture = None
    try:
        exif_a, exif_b = photo.exif['ExposureTime']
        if exif_b == 1:
            photo_shutter = '%s seconds' % exif_a
        else:
            photo_shutter = '%s/%s' % (exif_a, exif_b)
    except:
        photo_shutter = None
    try:
        focal_a, focal_b = photo.exif["FocalLength"]
        photo_focal = focal_a/focal_b
    except:
        photo_focal = None
    return render_template('photo.html', photo=photo, photo_aperture=photo_aperture, photo_shutter=photo_shutter,
                           photo_focal=photo_focal, paged=paged, gallery=gallery)
