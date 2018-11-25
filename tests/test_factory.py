from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_readKeys():
    app = create_app({'API_KEYS_FILE':'tests\\testKeys.txt'})
    #this should have found the file and read the key "test" into the config
    assert app.config.get('PLACES_KEY') == 'test'