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
def home_view():
    galleries = Gallery.objects
    return render_template('home.html', galleries=galleries)

@app.route('/gallery/<string:gallery_id>/')
def gallery_view(gallery_id):
    gallery = Gallery.objects.get_or_404(id=gallery_id)
    return render_template('gallery.html', gallery=gallery)

@app.route('/gallery/<string:gallery_id>/photo/<string:photo_id>/')
def photo_page_view(gallery_id, photo_id):
    photo = Photo.objects.get_or_404(id=photo_id)
    gallery = Gallery.objects.get_or_404(id=gallery_id)
    pos = gallery.photos.index(photo)
    paged = Gallery.objects.paginate_field('photos', gallery.id, pos+1, per_page=1, )
    aperture1, aperture2 = photo.exif["FNumber"]
    photo_aperture = aperture1/float(aperture2)
    exif_a, exif_b = photo.exif['ExposureTime']
    if exif_b == 1:
        photo_shutter = '%s seconds' % exif_a
    else:
        photo_shutter = '%s/%s' % (exif_a, exif_b)
    focal_a, focal_b = photo.exif["FocalLength"]
    photo_focal = focal_a/focal_b
    return render_template('photo.html', photo=photo, photo_aperture=photo_aperture, photo_shutter=photo_shutter,
                           photo_focal=photo_focal, paged=paged, gallery=gallery)
