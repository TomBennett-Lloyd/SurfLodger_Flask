import functools

from flask import (
    Flask, Blueprint, redirect, render_template, url_for, current_app
)

bp = Blueprint('home', __name__)

@bp.route('/home', methods=['GET'])
def home():
    if "PLACES_KEY" in current_app.config:
        jsFiles = ["js/mapping.js", "js/places.js"]
        jsFiles = current_app.config['JSFILES'] + jsFiles
        return render_template('home.html', jsFiles=jsFiles)
    else:
        return redirect(url_for('setKey.setKey'))
