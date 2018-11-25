import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #setup global config to hold paths to key files
    app.config.from_mapping(
        SECRET_KEY='dev',
        API_KEYS_FILE = 'flaskr/keys.txt',
        JSFILES=["external/JQuery/jquery-3.3.1.min.js", "external/Bootstrap/js/bootstrap.min.js"],
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #look for API Keys in API_KEYS_FILE
    if os.path.isfile(app.config['API_KEYS_FILE']):
        app = readKeys(app)

    #import blueprints
    from . import (setKey, home)
    app.register_blueprint(setKey.bp)
    app.register_blueprint(home.bp)

    return app

def readKeys(app):
    with open(app.config['API_KEYS_FILE'], 'r') as keys:
        for line in keys.readlines():
            if line.split(':')[0] == "places":
                app.config.update(
                    PLACES_KEY=line.split(':')[1],
                )
    return app
