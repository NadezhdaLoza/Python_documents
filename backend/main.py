from flask import Flask
from routes.routes import router
from utils.json_encoder import MongoJSONEncoder 
from flask_cors import CORS

app = Flask(__name__)
CORS(app, 
     origins=["http://localhost:8080", "http://127.0.0.1:8080"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

app.json = MongoJSONEncoder(app)
app.register_blueprint(router)

if __name__ == '__main__':
    app.run(debug=True)
