import pytest
import os
from helpers import redirectTest, checkRendered

def test_home(client, app):
    route = "/home"
    if "PLACES_KEY" in app.config:
        del app.config['PLACES_KEY']
    response = client.get(route)
    # there will be no key at this point should redirect to setKey page
    redirectTest(response, '/setKey')
    app.config.update(PLACES_KEY = 'test')
    response = client.get(route)
    #now there is a key there should be no redirect, check that the status code is 200 and
    #response contains html
    checkRendered(response)

