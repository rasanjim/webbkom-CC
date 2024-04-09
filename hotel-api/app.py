from flask import Flask, request
from flask_cors import CORS 

PORT=8322

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

@app.route("/")
def hello():
    return "<h1>Hello, Hotel-API!</h1>"

@app.route("/ip")
def ip():
    return { 'ip': request.remote_addr }

@app.route("/test", methods=['GET', 'POST'])
def test():
    return {
        'msg': "TESTING",
        'method': request.method
    }

@app.route("/test/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def testId(id):
    if request.method == 'GET':
        return {
        'msg': f"här får du id: {id}",
        'method': request.method
         }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
