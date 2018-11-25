import functools
from flask import (
    Blueprint, redirect, render_template, request, url_for, escape, current_app
)

bp = Blueprint('setKey', __name__)

@bp.route('/setKey', methods=['POST', 'GET'])
def setKey():
    #check app doesn't already have a key
    if hasattr(current_app.config, "PLACES_KEY"):
        return redirect(url_for('home'))

    #if this is a postback then update the key
    if request.method == 'POST':
        # no need to escape special characters as jinja does this in the template
        placesKey = request.form['places']
        # write to the file
        with open("keys.txt", "w") as keyFile:
            keyFile.write("places:"+placesKey)
        #update the application config
        current_app.config.update(
            PLACES_KEY=placesKey,
        )
        #redirect to the home page
        return redirect(url_for('home.home'))
    
    jsFiles = ["js/initialConfig.js"]
    jsFiles = current_app.config['JSFILES'] + jsFiles

    return render_template('setKey.html', jsFiles=jsFiles)
