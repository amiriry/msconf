import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.errorhandler(500)
def value_not_found(e):
    return "500"

@app.route("/healthy")
def hello_world():
    return json.dumps({"status": "OK"})

@app.route("/get_variable")
def get_env_value():
    try:
        value = os.environ['MY_ENVIRONMENT_VARIABLE']
    except (KeyError, TypeError) as exc:
        return 500
    mydict = {
            "variable": os.environ["MY_ENVIRONMENT_VARIABLE"]
    }
    return json.dumps(mydict)

@app.route('/set_variable', methods = ['POST'])
def set_env_var():
    os.environ['MY_ENVIRONMENT_VARIABLE'] = request.args.get('new')
    return ('', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
