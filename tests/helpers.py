def redirectTest(response, route):
    assert response.status_code == 302
    assert response.headers['location'] == 'http://localhost'+route


def redTestResponses(responses, route):
    for key in responses:
            redirectTest(responses[key], route)

def checkRendered (response):
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

def basicResponses (route,client):
    return {
        'post': client.post(route),
        'get': client.get(route)
    }
