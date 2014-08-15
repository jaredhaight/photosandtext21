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

@app.route('/photo/<string:photo_id>/')
def photo_page_view(photo_id):
    photo = Photo.objects.get_or_404(id=photo_id)
    return render_template('photo.html', photo=photo)
