from flask import Flask, render_template
from api.apiRoutes import api
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")

# Content-Disposition for file download
CORS(app, resources={r"/*": {"origins": "*"}},
     expose_headers=["Content-Disposition"])


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
