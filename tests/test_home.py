import pytest
import os
from helpers import redirectTest, checkRendered

def test_home(client, app):
    route = "/home"
    if "PLACES_KEY" in app.config:
        del app.config['PLACES_KEY']
    response = client.get(route)
    redirectTest(response, '/setKey')
    app.config.update(PLACES_KEY = 'test')
    response = client.get(route)
    checkRendered(response)

