from flask import Flask
from api.apiRoutes import api
from flask_cors import CORS

app = Flask(__name__, static_folder='./static', static_url_path='/static')
app.register_blueprint(api, url_prefix="/api")

# Content-Disposition for file download
CORS(app, resources={r"/*": {"origins": "*"}},
     expose_headers=["Content-Disposition"])


@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
