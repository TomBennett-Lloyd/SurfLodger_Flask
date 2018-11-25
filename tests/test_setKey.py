import pytest, os
from helpers import redirectTest, redTestResponses, checkRendered, basicResponses

def test_setKey (client, app):
    route = '/setKey'
    responses = basicResponses(route, client)
    
    if "PLACES_KEY" in app.config:
        #if there's already a key then redirect to the homepage
        redTestResponses(responses, '/home')
    else:
        #if no key then both requests without data should render the set key page
        for key in responses:
            checkRendered(responses[key])
        #the post request wth data should update the key and write it to file
        response = client.post(route, data={'places': 'test'})
        assert "PLACES_KEY" in app.config
        assert os.path.isfile(app.config['API_KEYS_FILE'])
        #retry the responses now there's a key in the config
        responses = basicResponses(route, client)
        redTestResponses(responses, '/home')
        #remove the key for preceeding tests
        del app.config['PLACES_KEY']
        #it should have redirected to the home page
        redirectTest(response, '/home')
        os.remove(app.config['API_KEYS_FILE'])




