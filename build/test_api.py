from rest_api import app
import os
import json

def test_healthy():
    response = app.test_client().get('/healthy')
    assert response.status_code == 200

def test_get_var():
    response = app.test_client().get('/get_variable')
    assert response.status_code == 200

def test_set_var():
    response1 = json.loads(app.test_client().get('/get_variable').data)
    old_val = str(response1['variable'])
    if old_val == 1:
        input_val = 2
    else:
        input_val = 2
    app.test_client().post("/set_variable?new=$input_val")
    response2 = json.loads(app.test_client().get('/get_variable').data)
    new_val = str(response2['variable'])
    assert old_val != new_val
