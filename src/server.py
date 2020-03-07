from flask import Flask, request, jsonify
app = Flask(__name__)

from utils import Worker
worker = Worker()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/response/', methods=['GET','POST'])
def get_response():
    if request.method == 'GET':
        return "We are live! Accepting POST requests for connection."

    if request.method == 'POST':
        # getting inputs
        name = str(request.form.get('name'))
        
        # response init
        response = {
            'status' : None,
            'message': None,
            'age'   : None
        }

        # input validation
        if any(v is None for v in [name]):
            # client problem
            response['status']  = False
            response['message'] = "Send all parameters"
            response['age']    = None
            return jsonify(response), 400

        status, age = worker.getAge()
        if status:
            # no problem
            response['status']  = True
            response['message'] = "OK"
            response['age']    = age
            return jsonify(response), 200
        else:
            # Worker problem
            response['status']  = False
            response['message'] = "Worker returned error"
            response['age']    = None
            return jsonify(response), 500


        return "We are live! Accepting requests for connection."

if __name__ == '__main__':
    app.run(debug=True,threaded=True,host='0.0.0.0',port='5000')


